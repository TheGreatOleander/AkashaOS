import { fetchHovatek } from './hovatek';
import { fetchAFH } from './afh';
import { fetchFirmware } from './firmware';

export async function fetchAllAdapters() {
  const hovatek = await fetchHovatek();
  const afh = await fetchAFH();
  const firmware = await fetchFirmware();
  return [...hovatek, ...afh, ...firmware];
}
