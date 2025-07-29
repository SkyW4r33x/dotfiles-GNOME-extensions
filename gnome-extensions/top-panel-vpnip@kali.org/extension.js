import { VPNIPAddressIndicator } from './VPNIPAddressIndicator.js';
import { Extension } from 'resource:///org/gnome/shell/extensions/extension.js';
import { panel } from 'resource:///org/gnome/shell/ui/main.js';

export default class VPNIpAddressExtension extends Extension {
    enable() {
        this._indicator = new VPNIPAddressIndicator();
        panel.addToStatusArea('vpn-ip-address-indicator', this._indicator);
    }

    disable() {
        this._indicator.destroy();
        this._indicator = null;
    }
}
