#!/bin/bash
set -e

# Install live-build
apt-get update
apt-get install -y live-build

# Set up live-build configuration
lb config \
   --architecture amd64 \
   --binary-images iso-hybrid \
   --distribution bullseye \
   --debian-installer live \
   --apt-recommends false \
   --bootappend-live "boot=live components"

# Copy installer script into the build
mkdir -p config/includes.chroot/build/config
cp /build/config/installer.py config/includes.chroot/build/config/installer.py

# Make sure scripts are executable
chmod +x /build/config/chroot.sh

# Include chroot script
mkdir -p config/hooks/live
cp /build/config/chroot.sh config/hooks/live/chroot.sh
