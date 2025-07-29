import St from 'gi://St';
import Clutter from 'gi://Clutter';
import GLib from 'gi://GLib';
import GObject from 'gi://GObject';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import * as Utils from './utils.js';

export class TargetInfoIndicator extends PanelMenu.Button {
    static {
        GObject.registerClass(this);
    }

    constructor() {
        super(0.0, "Target Info Indicator", true);

        this.hide();

        const box = new St.BoxLayout({ vertical: false });
        const targetIcon = new St.Icon({
            icon_name: 'mark-location',
            icon_size: 16,
        });

        this.buttonText = new St.Label({
            y_align: Clutter.ActorAlign.CENTER,
            style: 'margin-left: 6px;',
            text: 'Cargando...',
        });

        box.add_child(targetIcon);
        box.add_child(this.buttonText);
        this.add_child(box);

        this.connect('button-press-event', () => {
            if (this.ipAddress) {
                St.Clipboard.get_default().set_text(St.ClipboardType.CLIPBOARD, this.ipAddress);
            }
        });

        this.#updateLabel();
        this.#startAutoUpdate();
    }

    async #updateLabel() {
        try {
            const { ipAddress, machineName } = await Utils.getTargetInfo();
            if (ipAddress && machineName) {
                this.ipAddress = ipAddress;
                this.buttonText.set_text(`${ipAddress} - ${machineName}`);
                this.show();
            } else {
                this.ipAddress = null;
                this.buttonText.set_text('Sin Objetivo');
                this.show();
            }
        } catch (error) {
            this.ipAddress = null;
            this.buttonText.set_text('Sin Objetivo');
            this.show();
        }
    }

    #startAutoUpdate() {
        const refreshTime = 1;
        this._timeout = GLib.timeout_add_seconds(GLib.PRIORITY_DEFAULT, refreshTime, () => {
            this.#updateLabel();
            return GLib.SOURCE_CONTINUE;
        });
    }

    destroy() {
        if (this._timeout) {
            GLib.source_remove(this._timeout);
            this._timeout = null;
        }
        super.destroy();
    }
}
