# Pine A64 Gaming PC — Firmware / Config Files

This folder contains the reproducible configuration files used for the Pine A64 gaming PC software setup.

These files are committed to the repository so another person can review, copy, or reinstall the software environment on a freshly flashed DietPi image, instead of retyping commands from the devlog.

## Files

### `boot/dietpiEnv.txt`

DietPi boot environment configuration. Stores the display-related boot settings used during the project, including the `video=HDMI-A-1:1920x1080@60` resolution fix from Hour 6 that was required to leave enough shared memory (CMA) free for the hardware video decoder.

Target location on device:

```bash
/boot/dietpiEnv.txt
```

### `home/bashrc_moonlight_autostart`

Shell startup logic that automatically launches Moonlight after login on the main TTY, from Hours 8–11. This file is not named `.bashrc` in the repo to avoid overwriting a developer's own local shell config — during installation its contents are appended to the DietPi user's real `.bashrc`.

Target location on device:

```bash
/home/dietpi/.bashrc
```

### `udev/99-kms.rules`

udev rule used to expose KMS/DRM device access to the normal DietPi user (Hour 9), required so Moonlight can access the rendering/display devices without running as root.

Target location on device:

```bash
/etc/udev/rules.d/99-kms.rules
```

### `install.sh`

Helper script that backs up any existing config on the board and copies the repo-tracked files into place. Run from inside `firmware-config`:

```bash
chmod +x install.sh
sudo ./install.sh
```

After installation, edit `/home/dietpi/.bashrc` to replace `<HOSTNAME_OR_IP>` with your gaming PC's actual hostname or LAN IP, then reboot:

```bash
sudo reboot
```

## Note on `dietpiEnv.txt`

The copy in this repo is reconstructed from the Hour 6 devlog entry, not pulled directly off the board. Boot environment files can carry board-specific arguments, so before trusting it, pull the exact known-good version off your own Pine A64 and overwrite this file with it:

```bash
cp /boot/dietpiEnv.txt firmware-config/boot/dietpiEnv.txt
```
