#!/bin/bash
set -e

# Install necessary packages
apt-get update
apt-get install -y \
    xorg \
    xinit \
    openbox \
    python3 \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0 \
    network-manager \
    ca-certificates \
    curl \
    wget \
    gnupg \
    apt-transport-https \
    software-properties-common

# Create a user (for security)
useradd -m -s /bin/bash ociuser
echo 'ociuser:password' | chpasswd
usermod -aG sudo ociuser

# Copy the installer script
mkdir -p /home/ociuser/installer
cp /build/config/installer.py /home/ociuser/installer/
chown -R ociuser:ociuser /home/ociuser/installer

# Set up Openbox autostart to launch the installer
mkdir -p /home/ociuser/.config/openbox
cat <<EOF > /home/ociuser/.config/openbox/autostart
python3 /home/ociuser/installer/installer.py
EOF
chown -R ociuser:ociuser /home/ociuser/.config

# Set up the installer to run on boot
cat <<EOF > /etc/systemd/system/installer.service
[Unit]
Description=OCI Linux Installer
After=network.target

[Service]
Type=simple
User=ociuser
ExecStart=/usr/bin/startx /usr/bin/openbox-session
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl enable installer.service
systemctl enable NetworkManager.service

# Clean up
apt-get clean
