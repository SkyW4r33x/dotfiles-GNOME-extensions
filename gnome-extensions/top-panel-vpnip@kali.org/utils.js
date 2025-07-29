import GLib from 'gi://GLib';
import Gio from 'gi://Gio';

// Promisificar la función
Gio._promisify(Gio.Subprocess.prototype, 'communicate_utf8_async');

export const getVpnIp = async () => {
    try {
        // Comando para obtener la IP de la VPN
        const ipCommand = ['sh', '-c', 'ip a show "$(ip tuntap show | cut -d : -f1 | head -n 1)" 2>/dev/null'];
        
        const ipProc = new Gio.Subprocess({
            argv: ipCommand,
            flags: Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
        });
        
        ipProc.init(null);
        
        let [ipOutput, ipError] = await ipProc.communicate_utf8_async(null, null);
        
        // Si hay error o no hay output, retornar null
        if (ipError || !ipOutput || ipOutput.trim() === '') {
            return null;
        }
        
        // Buscar la IP en el output
        const ipMatch = ipOutput.match(/inet (\d{1,3}(?:\.\d{1,3}){3})/);
        
        if (ipMatch && ipMatch[1]) {
            return ipMatch[1];
        } else {
            return null;
        }
    } catch (error) {
        console.error(`Error obteniendo IP de VPN: ${error.message}`);
        return null;
    }
};
