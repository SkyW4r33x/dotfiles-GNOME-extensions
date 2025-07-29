import GLib from 'gi://GLib';
import Gio from 'gi://Gio';

Gio._promisify(Gio.Subprocess.prototype, 'communicate_utf8_async');

export const getLocalIp = async () => {
    // Usamos un comando más simple y confiable
    const ipCommand = ['sh', '-c', 'ip route get 1.1.1.1 | grep -oP "src \\K\\S+" 2>/dev/null || hostname -I | cut -d" " -f1'];
    
    const ipProc = new Gio.Subprocess({
        argv: ipCommand,
        flags: Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
    });
    ipProc.init(null);
    
    try {
        let [ipOutput, stderr] = await ipProc.communicate_utf8_async(null, null);
        
        if (ipOutput && ipOutput.trim()) {
            return ipOutput.trim();
        }
        
        return null;
        
    } catch (error) {
        return null;
    }
};

// Función alternativa más simple (por si se necesita)
export const getLocalIpSimple = async () => {
    const hostnameCommand = ['hostname', '-I'];
    
    const hostnameProc = new Gio.Subprocess({
        argv: hostnameCommand,
        flags: Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
    });
    hostnameProc.init(null);
    
    try {
        let [output, stderr] = await hostnameProc.communicate_utf8_async(null, null);
        
        if (output && output.trim()) {
            // hostname -I puede devolver múltiples IPs, tomamos la primera
            return output.trim().split(' ')[0];
        }
        
        return null;
        
    } catch (error) {
        return null;
    }
};

// Función para obtener información de interfaces de red (opcional para debugging)
export const getNetworkInterfaces = async () => {
    const interfacesCommand = ['sh', '-c', 'ip link show | grep -E "^[0-9]+:" | cut -d: -f2 | tr -d " "'];
    
    const interfacesProc = new Gio.Subprocess({
        argv: interfacesCommand,
        flags: Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
    });
    interfacesProc.init(null);
    
    try {
        let [output, stderr] = await interfacesProc.communicate_utf8_async(null, null);
        return output ? output.trim().split('\n') : [];
    } catch (error) {
        return [];
    }
};
