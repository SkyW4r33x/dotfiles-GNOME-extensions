import { TargetInfoIndicator } from './TargetInfoIndicator.js';
import { Extension } from 'resource:///org/gnome/shell/extensions/extension.js';
import { panel } from 'resource:///org/gnome/shell/ui/main.js';

export default class TargetInfoExtension extends Extension {
    enable() {
        this._indicator = new TargetInfoIndicator();
        panel.addToStatusArea('top-panel-target-indicator', this._indicator);
    }

    disable() {
        this._indicator.destroy();
        this._indicator = null;
    }
}
