import GLib from 'gi://GLib';
import Gio from 'gi://Gio';

export const getTargetInfo = async () => {
    const filePath = GLib.build_filenamev([GLib.get_home_dir(), '.config', 'bin', 'target', 'target.txt']);
    const file = Gio.File.new_for_path(filePath);

    try {
        if (file.query_exists(null)) {
            const [success, contents] = file.load_contents(null);
            if (success) {
                const [ipAddress, machineName] = new TextDecoder().decode(contents).trim().split(/\s+/);
                if (ipAddress && machineName) {
                    return { ipAddress, machineName };
                }
            }
        }
        return { ipAddress: null, machineName: null };
    } catch (error) {
        console.error(`Error reading target.txt: ${error.message}`);
        return { ipAddress: null, machineName: null };
    }
};
