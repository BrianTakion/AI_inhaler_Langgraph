// Device Selector Component

import { DeviceType } from '../types/analysis.js';

const devices: DeviceType[] = [
  { 
    id: 'DPI', 
    name: 'DPI', 
    description: 'Dry Powder Inhaler (건조분말흡입기)' 
  },
  { 
    id: 'pMDI', 
    name: 'pMDI', 
    description: 'Pressurized Metered Dose Inhaler (정량분무흡입기)' 
  },
  { 
    id: 'SMI', 
    name: 'SMI', 
    description: 'Soft Mist Inhaler (연무흡입기)' 
  }
];

export class DeviceSelector {
  private deviceBtn: HTMLButtonElement;
  private dropdown: HTMLElement;
  private selectedDevice: DeviceType | null = null;
  private onSelectCallback?: (device: DeviceType) => void;

  constructor() {
    this.deviceBtn = document.getElementById('deviceSelect') as HTMLButtonElement;
    this.dropdown = document.getElementById('deviceDropdown') as HTMLElement;
    this.init();
  }

  private init(): void {
    // Toggle dropdown
    this.deviceBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleDropdown();
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', () => {
      this.hideDropdown();
    });

    // Device selection
    const dropdownItems = this.dropdown.querySelectorAll('.dropdown-item');
    dropdownItems.forEach(item => {
      item.addEventListener('click', (e) => {
        e.stopPropagation();
        const deviceId = (item as HTMLElement).dataset.deviceId as DeviceType['id'];
        const device = devices.find(d => d.id === deviceId);
        if (device) {
          this.selectDevice(device);
        }
      });
    });
  }

  private toggleDropdown(): void {
    const isVisible = this.dropdown.style.display !== 'none';
    if (isVisible) {
      this.hideDropdown();
    } else {
      this.showDropdown();
    }
  }

  private showDropdown(): void {
    this.dropdown.style.display = 'block';
    this.deviceBtn.classList.add('active');
  }

  private hideDropdown(): void {
    this.dropdown.style.display = 'none';
    this.deviceBtn.classList.remove('active');
  }

  private selectDevice(device: DeviceType): void {
    this.selectedDevice = device;
    
    // Update UI - mark selected item
    const dropdownItems = this.dropdown.querySelectorAll('.dropdown-item');
    dropdownItems.forEach(item => {
      const itemDeviceId = (item as HTMLElement).dataset.deviceId;
      if (itemDeviceId === device.id) {
        item.classList.add('selected');
      } else {
        item.classList.remove('selected');
      }
    });

    // Hide dropdown
    this.hideDropdown();

    // Trigger callback
    if (this.onSelectCallback) {
      this.onSelectCallback(device);
    }
  }

  public onSelect(callback: (device: DeviceType) => void): void {
    this.onSelectCallback = callback;
  }

  public getSelectedDevice(): DeviceType | null {
    return this.selectedDevice;
  }

  public reset(): void {
    this.selectedDevice = null;
    const dropdownItems = this.dropdown.querySelectorAll('.dropdown-item');
    dropdownItems.forEach(item => item.classList.remove('selected'));
  }
}

