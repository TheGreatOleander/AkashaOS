# Android Service Lab

> A browser-based Android device servicing tool leveraging WebUSB and WebSerial APIs for Fastboot, ADB, and UART communications.

## 🚀 Overview

Android Service Lab is a cutting-edge web application that brings Android device servicing capabilities directly to your browser. No more installing platform-tools or dealing with driver issues - this tool uses modern web APIs to communicate with Android devices for debugging, flashing, and recovery operations.

### Key Features

- **🔌 Fastboot over WebUSB**: Query device variables and execute fastboot commands
- **📱 ADB Integration**: Skeleton implementation with CNXN handshake support  
- **⚡ UART/Serial Communication**: MTK Preloader and Qualcomm EDL mode support via WebSerial
- **🔍 Real-time Logging**: Comprehensive hex dump and activity monitoring
- **🛡️ Safe Operations**: Built-in reconnection logic and error handling
- **🌐 Pure Browser**: No drivers or native tools required*

*Some Windows configurations may require WinUSB driver binding via Zadig

## 🎯 Supported Use Cases

### Fastboot Operations
- Device identification (`getvar:product`)
- Bootloader unlocking preparation
- Recovery mode interactions
- Custom ROM flashing workflows

### ADB Communications  
- Device handshake and authentication
- Shell command execution (roadmap)
- File push/pull operations (roadmap)

### UART/Serial Console
- MTK Preloader communication
- Qualcomm EDL (Emergency Download) mode
- Bootrom console access
- Debug output monitoring

## 🔧 Compatible Devices

### Tested Fastboot Targets
- **Google Pixels** (all generations)
- **Motorola devices** (most models)  
- **OnePlus devices** (selected models)
- **ASUS devices** (ROG Phone series, Zenfone)
- **HMD/Nokia** Android devices

### Serial/UART Support
- **MTK MediaTek** devices in Preloader mode
- **Qualcomm** devices in EDL mode  
- **CDC-ACM UART adapters** (PL2303, CH340, CP210x)

## 🚀 Getting Started

### Prerequisites
- Modern browser with WebUSB and WebSerial support:
  - Chrome 89+ / Edge 89+
  - Opera 76+
  - *Note: Firefox and Safari not supported due to API limitations*

### Installation

1. Clone the repository:
```bash
git clone https://github.com/TheGreatOleander/One_at_a_Time_Machine.git
cd One_at_a_Time_Machine
```

2. Install dependencies:
```bash
npm install react react-dom
```

3. Set up your build environment (Next.js, Vite, or Create React App)

4. Import and use the component:
```jsx
import AndroidServiceLab from './android_service_lab_browser_mvp_web_usb_web_serial.jsx';

function App() {
  return <AndroidServiceLab />;
}
```

### Quick Start Guide

#### Fastboot Mode
1. Boot your device into fastboot mode:
   - Power off device
   - Hold `Volume Down + Power` (varies by device)
   - Connect via USB

2. Click **"Connect Fastboot"** in the web interface
3. Select your device from the browser's USB chooser
4. Click **"getvar:product"** to test communication

#### ADB Mode  
1. Enable Developer Options and USB Debugging on your device
2. Connect via USB and authorize the computer
3. Click **"Connect ADB"** 
4. Try the **"CNXN handshake"** to establish connection

#### Serial/UART Mode
1. Connect your UART adapter or put device in preloader/EDL mode
2. Click **"Open Serial"** and select the appropriate port
3. Use the input field to send commands
4. Monitor responses in the log pane

## 🛠️ Technical Architecture

### Core Technologies
- **React 18+** with hooks for state management
- **WebUSB API** for direct USB device communication
- **WebSerial API** for UART/serial port access
- **TypeScript/JSX** for type safety and component structure

### Protocol Implementations

#### Fastboot Protocol
```javascript
// Command structure: "getvar:<variable_name>"
const cmd = encoder.encode(`getvar:${key}`);
await device.transferOut(epOut.endpointNumber, cmd);
```

#### ADB Protocol Skeleton  
```javascript
// 24-byte header + payload
const ADB_CONST = {
  SYNC: 0x434e5953,
  CNXN: 0x4e584e43,
};
```

#### Serial Communication
```javascript  
// 115200 baud default, configurable
await port.open({ baudRate: 115200 });
```

## 🔐 Security & Safety

⚠️ **Important**: Only use this tool on devices you own or have explicit permission to modify. Unauthorized device modification may:
- Void warranties
- Brick devices  
- Violate local laws
- Compromise device security

### Safe Practices
- Always backup critical partitions before flashing
- Verify device compatibility before operations
- Use appropriate cables and connections
- Monitor log output for errors

## 🚧 Development Roadmap

### Planned Features
- **Full ADB Implementation**: Authentication, shell commands, file operations
- **Enhanced Fastboot**: Flash operations, partition management
- **MTK DA Support**: Download Agent handshake via WebUSB
- **Qualcomm Firehose**: Sahara protocol implementation
- **Native Helper Bridge**: WebSocket fallback for unsupported devices
- **Batch Operations**: Script-based automation support

### Contributing
Contributions are welcome! This is an educational MVP with room for expansion:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Windows Driver Issues
If the browser cannot access your device:
1. Download and run [Zadig](https://zadig.akeo.ie/)
2. Select your device in fastboot/adb mode
3. Replace the driver with WinUSB
4. Restart browser and try again

### Device Not Detected
- Ensure USB debugging is enabled (for ADB)
- Try different USB cables (data cables, not charge-only)
- Check device is in correct mode (fastboot/adb/preloader)
- Verify browser supports WebUSB/WebSerial

### Connection Timeouts
- Some devices require specific timing or initialization sequences
- Check the log output for protocol-specific error messages
- Try disconnecting and reconnecting the device

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚡ Acknowledgments

- WebUSB and WebSerial API communities
- Android platform-tools developers  
- MTK and Qualcomm protocol documentation contributors
- Open source Android development community

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check existing documentation and troubleshooting guides
- Ensure you're using a compatible browser and device

---

**Made with ❤️ by TheGreatOleander**

*Bringing Android device servicing to the modern web*