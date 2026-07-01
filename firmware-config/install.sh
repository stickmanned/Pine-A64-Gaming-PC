#!/usr/bin/env bash

set -euo pipefail

echo "Installing Pine A64 Gaming PC firmware/config files..."

if [ "$(id -u)" -ne 0 ]; then
    echo "Error: this installer must be run with sudo or as root."
    exit 1
fi

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DIETPI_USER="dietpi"
DIETPI_HOME="/home/${DIETPI_USER}"

echo "Backing up existing config files..."

if [ -f /boot/dietpiEnv.txt ]; then
    cp /boot/dietpiEnv.txt /boot/dietpiEnv.txt.backup
    echo "Backed up /boot/dietpiEnv.txt to /boot/dietpiEnv.txt.backup"
fi

if [ -f "${DIETPI_HOME}/.bashrc" ]; then
    cp "${DIETPI_HOME}/.bashrc" "${DIETPI_HOME}/.bashrc.backup"
    echo "Backed up ${DIETPI_HOME}/.bashrc to ${DIETPI_HOME}/.bashrc.backup"
fi

if [ -f /etc/udev/rules.d/99-kms.rules ]; then
    cp /etc/udev/rules.d/99-kms.rules /etc/udev/rules.d/99-kms.rules.backup
    echo "Backed up existing 99-kms.rules"
fi

echo "Installing boot configuration..."
cp "${REPO_DIR}/boot/dietpiEnv.txt" /boot/dietpiEnv.txt

echo "Installing udev rule..."
cp "${REPO_DIR}/udev/99-kms.rules" /etc/udev/rules.d/99-kms.rules

echo "Appending Moonlight autostart block to ${DIETPI_HOME}/.bashrc..."

if ! grep -q "PINE_A64_MOONLIGHT_AUTOSTART_BEGIN" "${DIETPI_HOME}/.bashrc" 2>/dev/null; then
    cat "${REPO_DIR}/home/bashrc_moonlight_autostart" >> "${DIETPI_HOME}/.bashrc"
else
    echo "Moonlight autostart block already exists in .bashrc; skipping append."
fi

chown "${DIETPI_USER}:${DIETPI_USER}" "${DIETPI_HOME}/.bashrc"

echo "Reloading udev rules..."
udevadm control --reload-rules
udevadm trigger

echo "Install complete."
echo "Edit ${DIETPI_HOME}/.bashrc to replace <HOSTNAME_OR_IP> with your gaming PC's address."
echo "Reboot the Pine A64 with: sudo reboot"
