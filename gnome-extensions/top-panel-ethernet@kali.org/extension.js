import { LocalIpIndicator } from './LocalIpIndicator.js';
import { Extension } from 'resource:///org/gnome/shell/extensions/extension.js';
import { panel } from 'resource:///org/gnome/shell/ui/main.js';

export default class LocalIpExtension extends Extension {
    enable() {
        this._indicator = new LocalIpIndicator();
        panel.addToStatusArea('top-panel-localip-indicator', this._indicator);
    }

    disable() {
        this._indicator.destroy();
        this._indicator = null;
    }
}
