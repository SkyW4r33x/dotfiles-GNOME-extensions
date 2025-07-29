import St from 'gi://St';
import Clutter from 'gi://Clutter';
import GLib from 'gi://GLib';
import Gio from 'gi://Gio';
import GObject from 'gi://GObject';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import * as Utils from './utils.js';

export class VPNIPAddressIndicator extends PanelMenu.Button {
    static {
        GObject.registerClass(this);
    }

    constructor() {
        super(0.0, "VPN IP Address Indicator", true);

        const box = new St.BoxLayout({ vertical: false });
        const vpnIcon = new St.Icon({
            icon_name: 'draw-cuboid',
            icon_size: 16,
        });

        this.buttonText = new St.Label({
            y_align: Clutter.ActorAlign.CENTER,
            style: 'margin-left: 6px;',
            text: 'Cargando...',
        });

        box.add_child(vpnIcon);
        box.add_child(this.buttonText);
        this.add_child(box);

        this.connect('button-press-event', () => {
            if (!this.vpnIp) return;
            St.Clipboard.get_default().set_text(St.ClipboardType.CLIPBOARD, this.vpnIp);
        });

        this.show();
        this.#updateLabel();
        this.#startAutoUpdate();
    }

    async #updateLabel() {
        try {
            if (typeof Utils.getVpnIp !== 'function') {
                this.buttonText.set_text('Error');
                return;
            }

            this.vpnIp = await Utils.getVpnIp();
            
            if (this.vpnIp) {
                this.buttonText.set_text(this.vpnIp);
            } else {
                this.buttonText.set_text('Desconectado');
                this.vpnIp = null;
            }
        } catch (error) {
            this.buttonText.set_text('Error');
            this.vpnIp = null;
        }
    }

    #startAutoUpdate() {
        const refreshTime = 3;

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
