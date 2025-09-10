import React, { useEffect, useRef, useState } from "react";

// Minimal, single-file React app that demonstrates a browser-based Android service tool MVP
// - Fastboot over WebUSB ("getvar:product" test)
// - ADB (skeleton) over WebUSB with CNXN handshake outline
// - MTK/Qualcomm UART (preloader/EDL) port discovery via Web Serial
// - Log pane, hex dump, and safe reconnect logic
//
// Notes:
// • WebUSB requires WinUSB/libusb-like driver on Windows for vendor interfaces. Zadig can help bind.
// • WebSerial works with CDC-ACM (UART) adapters (PL2303, CH340, CP210x) and some MTK Preloader ports if exposed as CDC.
// • This is an educational MVP. Implementations of flashing/unlock/etc. are intentionally omitted.
// • Tested targets you can try:
//   - Fastboot: most Pixels, many Motorolas, some OnePlus, ASUS devices in fastboot mode
//   - ADB: devices that expose a WebUSB-compatible interface (not universal). Otherwise use the local-bridge approach.
//
// Security: only operate on hardware you own or have permission to service.

// --- Helpers --------------------------------------------------------------
const encoder = new TextEncoder();
const decoder = new TextDecoder();

function toHex(arr: Uint8Array, max = 512) {
  const len = Math.min(arr.length, max);
  let s = "";
  for (let i = 0; i < len; i++) s += arr[i].toString(16).padStart(2, "0") + (i % 16 === 15 ? "\n" : " ");
  if (arr.length > len) s += `\n… +${arr.length - len} bytes`;
  return s;
}

// Fastboot protocol utils (very small subset)
async function fastbootGetVar(device: USBDevice, iface: USBInterface, epIn: USBEndpoint, epOut: USBEndpoint, key: string) {
  // Command is ASCII: "getvar:<key>"
  const cmd = encoder.encode(`getvar:${key}`);
  await device.transferOut(epOut.endpointNumber, cmd);
  const resp = await device.transferIn(epIn.endpointNumber, 512);
  if (!resp.data) throw new Error("No data from device");
  const text = decoder.decode(resp.data.buffer);
  return text.trim();
}

// Very tiny ADB skeleton: just sends CNXN and expects a banner. Full ADB is more involved.
// This shows structure; a production tool should use a complete ADB implementation.
const ADB_CONST = {
  SYNC: 0x434e5953,
  CNXN: 0x4e584e43,
};

function adbPacket(cmd: number, arg0 = 0x01000000, arg1 = 0, payload = new Uint8Array()) {
  // ADB packet header is 24 bytes
  const buf = new ArrayBuffer(24 + payload.length);
  const v = new DataView(buf);
  const u8 = new Uint8Array(buf);
  v.setUint32(0, cmd, true);
  v.setUint32(4, arg0, true);
  v.setUint32(8, arg1, true);
  v.setUint32(12, payload.length, true);
  // checksum = sum of payload bytes
  let sum = 0; for (let i = 0; i < payload.length; i++) sum += payload[i];
  v.setUint32(16, sum >>> 0, true);
  v.setUint32(20, cmd ^ 0xffffffff, true);
  u8.set(payload, 24);
  return u8;
}

async function adbCnxn(device: USBDevice, epIn: USBEndpoint, epOut: USBEndpoint) {
  const systemIdentity = encoder.encode("host::webusb\0");
  const pkt = adbPacket(ADB_CONST.CNXN, 0x01000000, 0, systemIdentity);
  await device.transferOut(epOut.endpointNumber, pkt);
  const res = await device.transferIn(epIn.endpointNumber, 1024);
  if (!res.data) throw new Error("No ADB response");
  return toHex(new Uint8Array(res.data.buffer));
}

export default function AndroidServiceLab() {
  const [log, setLog] = useState<string>("");
  const [usbDevice, setUsbDevice] = useState<USBDevice | null>(null);
  const [ifaceInfo, setIfaceInfo] = useState<{ iface: USBInterface; epIn: USBEndpoint; epOut: USBEndpoint } | null>(null);
  const [serialPort, setSerialPort] = useState<SerialPort | null>(null);
  const [serialOpen, setSerialOpen] = useState(false);

  function append(msg: string) {
    setLog((l) => l + (l ? "\n" : "") + msg);
  }

  // --- WebUSB: Request device & claim interface -------------------------
  async function requestFastboot() {
    try {
      const device = await navigator.usb.requestDevice({ filters: [
        // Broad fastboot matches; many devices present vendor-specific class 255 during fastboot.
        // We cannot enumerate all vendor IDs here, but letting the chooser show all is okay.
        { vendorId: 0x18d1 }, // Google
        { vendorId: 0x0b05 }, // ASUS
        { vendorId: 0x2b4c }, // OnePlus
        { vendorId: 0x22b8 }, // Motorola
        { vendorId: 0x2a70 }, // HMD/Nokia
      ]});
      await device.open();
      if (device.configuration == null) await device.selectConfiguration(1);
      // Heuristic: find first interface with 2 bulk endpoints
      let chosen: { iface: USBInterface; epIn: USBEndpoint; epOut: USBEndpoint } | null = null;
      for (const cfg of device.configurations) {
        for (const iface of cfg.interfaces) {
          for (const alt of iface.alternates) {
            const eps = alt.endpoints.filter((e) => e.type === "bulk");
            const epIn = eps.find((e) => e.direction === "in");
            const epOut = eps.find((e) => e.direction === "out");
            if (epIn && epOut) {
              await device.claimInterface(iface.interfaceNumber);
              await device.selectAlternateInterface(iface.interfaceNumber, alt.alternateSetting);
              chosen = { iface: iface, epIn, epOut } as any;
              break;
            }
          }
          if (chosen) break;
        }
        if (chosen) break;
      }
      if (!chosen) throw new Error("No bulk in/out endpoints found");
      setUsbDevice(device);
      setIfaceInfo(chosen);
      append(`Fastboot device ready: ${device.productName || "Unknown"}`);
    } catch (e: any) {
      append(`Fastboot connect error: ${e.message || e}`);
    }
  }

  async function doFastbootGetVarProduct() {
    try {
      if (!usbDevice || !ifaceInfo) throw new Error("No device");
      const out = await fastbootGetVar(usbDevice, ifaceInfo.iface, ifaceInfo.epIn, ifaceInfo.epOut, "product");
      append(`fastboot getvar:product => ${out}`);
    } catch (e: any) {
      append(`Fastboot getvar error: ${e.message || e}`);
    }
  }

  // --- WebUSB ADB (skeleton) -------------------------------------------
  async function requestAdb() {
    try {
      const device = await navigator.usb.requestDevice({ filters: [
        { vendorId: 0x18d1 }, { vendorId: 0x0b05 }, { vendorId: 0x2b4c }, { vendorId: 0x22b8 }, { vendorId: 0x2a70 },
      ]});
      await device.open();
      if (device.configuration == null) await device.selectConfiguration(1);
      // Some ADB implementations expose bulk endpoints similarly; otherwise, a helper bridge is recommended.
      let chosen: { iface: USBInterface; epIn: USBEndpoint; epOut: USBEndpoint } | null = null;
      for (const cfg of device.configurations) {
        for (const iface of cfg.interfaces) {
          for (const alt of iface.alternates) {
            const eps = alt.endpoints.filter((e) => e.type === "bulk");
            const epIn = eps.find((e) => e.direction === "in");
            const epOut = eps.find((e) => e.direction === "out");
            if (epIn && epOut) {
              await device.claimInterface(iface.interfaceNumber);
              await device.selectAlternateInterface(iface.interfaceNumber, alt.alternateSetting);
              chosen = { iface: iface, epIn, epOut } as any;
              break;
            }
          }
          if (chosen) break;
        }
        if (chosen) break;
      }
      if (!chosen) throw new Error("No bulk in/out endpoints found for ADB");
      setUsbDevice(device);
      setIfaceInfo(chosen);
      append(`ADB candidate ready: ${device.productName || "Unknown"}`);
    } catch (e: any) {
      append(`ADB connect error: ${e.message || e}`);
    }
  }

  async function doAdbHandshake() {
    try {
      if (!usbDevice || !ifaceInfo) throw new Error("No device");
      const hex = await adbCnxn(usbDevice, ifaceInfo.epIn, ifaceInfo.epOut);
      append(`ADB CNXN response (hex):\n${hex}`);
    } catch (e: any) {
      append(`ADB handshake error: ${e.message || e}`);
    }
  }

  // --- WebSerial: Discover and open serial ports ------------------------
  async function requestSerial() {
    try {
      const port = await navigator.serial.requestPort({
        filters: [
          // Optional VID/PID filters for known UARTs; leaving empty lets user choose any serial device
        ],
      });
      await port.open({ baudRate: 115200 });
      setSerialPort(port);
      setSerialOpen(true);
      append("Serial port opened (115200). Try MTK preloader or EDL UART consoles.");
      readSerial(port);
    } catch (e: any) {
      append(`Serial error: ${e.message || e}`);
    }
  }

  async function readSerial(port: SerialPort) {
    try {
      const reader = port.readable?.getReader();
      if (!reader) return;
      // eslint-disable-next-line no-constant-condition
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        if (value) append("[SERIAL] " + decoder.decode(value));
      }
      reader.releaseLock();
    } catch (e: any) {
      append(`Serial read error: ${e.message || e}`);
    }
  }

  async function writeSerial(text: string) {
    if (!serialPort || !serialPort.writable) return;
    const writer = serialPort.writable.getWriter();
    await writer.write(encoder.encode(text));
    writer.releaseLock();
  }

  async function closeSerial() {
    try {
      await serialPort?.close();
      setSerialOpen(false);
      append("Serial port closed.");
    } catch {}
  }

  // --- UI ---------------------------------------------------------------
  const [serialInput, setSerialInput] = useState("");

  return (
    <div className="min-h-screen w-full bg-slate-50 text-slate-900 p-6">
      <div className="max-w-5xl mx-auto grid gap-4">
        <header className="flex items-baseline justify-between">
          <h1 className="text-2xl md:text-3xl font-bold">Android Service Lab — Browser MVP</h1>
          <div className="text-sm opacity-70">WebUSB · WebSerial · React</div>
        </header>

        <section className="grid md:grid-cols-2 gap-4">
          <div className="p-4 rounded-2xl shadow bg-white">
            <h2 className="font-semibold mb-2">Fastboot (WebUSB)</h2>
            <p className="text-sm mb-3">Connect a device in Fastboot mode and query a variable.</p>
            <div className="flex gap-2">
              <button onClick={requestFastboot} className="px-3 py-2 rounded-xl shadow bg-slate-900 text-white">Connect Fastboot</button>
              <button onClick={doFastbootGetVarProduct} className="px-3 py-2 rounded-xl shadow bg-slate-200">getvar:product</button>
            </div>
          </div>

          <div className="p-4 rounded-2xl shadow bg-white">
            <h2 className="font-semibold mb-2">ADB (WebUSB) — skeleton</h2>
            <p className="text-sm mb-3">Attempt CNXN handshake. Many devices require a local bridge app instead of pure WebUSB.</p>
            <div className="flex gap-2">
              <button onClick={requestAdb} className="px-3 py-2 rounded-xl shadow bg-slate-900 text-white">Connect ADB</button>
              <button onClick={doAdbHandshake} className="px-3 py-2 rounded-xl shadow bg-slate-200">CNXN handshake</button>
            </div>
          </div>

          <div className="p-4 rounded-2xl shadow bg-white md:col-span-2">
            <h2 className="font-semibold mb-2">UART / Preloader / EDL (WebSerial)</h2>
            <p className="text-sm mb-3">Open a serial console at 115200 baud (adjust per target). Works with CDC-ACM adapters and some device bootrom consoles.</p>
            <div className="flex gap-2 mb-3">
              <button onClick={requestSerial} className="px-3 py-2 rounded-xl shadow bg-slate-900 text-white">Open Serial</button>
              <button onClick={closeSerial} className="px-3 py-2 rounded-xl shadow bg-slate-200">Close</button>
            </div>
            <div className="flex gap-2">
              <input value={serialInput} onChange={(e) => setSerialInput(e.target.value)} placeholder="Type and send…" className="flex-1 px-3 py-2 rounded-xl border" />
              <button onClick={() => { writeSerial(serialInput + "\r\n"); setSerialInput(""); }} className="px-3 py-2 rounded-xl shadow bg-slate-200">Send</button>
            </div>
          </div>
        </section>

        <section className="p-4 rounded-2xl shadow bg-white">
          <h2 className="font-semibold mb-2">Log</h2>
          <pre className="text-xs whitespace-pre-wrap bg-slate-50 rounded-xl p-3 max-h-80 overflow-auto">{log || "(logs will appear here)"}</pre>
        </section>

        <footer className="text-xs opacity-70">
          <p>Tip: On Windows, use a driver switcher (e.g., Zadig) to bind WinUSB for fastboot/adb interfaces if the chooser cannot claim the device.</p>
          <p>Roadmap: add full ADB (auth, shell, push/pull), fastboot flash/read, MTK DA handshake (WebUSB) with user-supplied DA, Qualcomm Sahara/Firehose over USB bulk, plus a native helper fallback via WebSocket.</p>
        </footer>
      </div>
    </div>
  );
}
