# Pine A64 Gaming PC — Firmware / Config Files

This folder contains the reproducible configuration files used for the Pine A64 gaming PC software setup.

These files are committed to the repository so another person can review, copy, or reinstall the software environment on a freshly flashed DietPi image, instead of retyping commands from the devlog.

## Files

### `boot/dietpiEnv.txt`

DietPi boot environment snippet. Stores the display-related boot setting used during the project: `video=HDMI-A-1:1920x1080@60`. This Hour 6 fix caps HDMI at 1080p before Linux starts, which keeps the Allwinner A64 DRM/KMS display stack from exhausting the CMA memory pool and blocking Moonlight's hardware-accelerated path.

Target location on device:

```bash
/boot/dietpiEnv.txt
```

Do not blindly replace a board's known-good `/boot/dietpiEnv.txt` with a hand-typed file. Back it up first, then merge this repo's `video=HDMI-A-1:1920x1080@60` line into the existing file. The installer does this merge automatically and writes `/boot/dietpiEnv.txt.backup` before changing anything.

### `home/bashrc_moonlight_autostart`

Shell startup logic that automatically launches Moonlight after login on the main TTY, from Hours 8–11. This file is not named `.bashrc` in the repo to avoid overwriting a developer's own local shell config — during installation its contents are appended to the DietPi user's real `.bashrc`.

Target location on device:

```bash
/home/dietpi/.bashrc
```

### `udev/99-kms.rules`

udev rule used to expose KMS/DRM and input device access to the normal DietPi user (Hour 9), required so Moonlight can access the rendering/display and mouse/keyboard devices without running as root.

Target location on device:

```bash
/etc/udev/rules.d/99-kms.rules
```

### `install.sh`

Helper script that backs up existing config on the board, merges the tracked HDMI cap into `/boot/dietpiEnv.txt`, installs the udev rule, and appends the Moonlight autostart block. Run from inside `firmware-config`:

```bash
chmod +x install.sh
sudo ./install.sh
```

After installation, edit `/home/dietpi/.bashrc` to replace `<HOSTNAME_OR_IP>` with your gaming PC's actual hostname or LAN IP, then reboot:

```bash
sudo reboot
```
