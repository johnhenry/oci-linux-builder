# Use an official Debian image as the base, specifying the amd64 architecture
FROM --platform=linux/amd64 debian:bullseye

# Set environment variables for non-interactive installs
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages for live-build and development
RUN apt-get update && \
    apt-get install -y \
        live-build \
        syslinux \
        xorriso \
        cpio \
        python3 \
        python3-gi \
        python3-gi-cairo \
        gir1.2-gtk-3.0 \
        vim nano # Text editors for development

# Set working directory
WORKDIR /build

# Copy build scripts and configurations
COPY config /build/config

# Make scripts executable
RUN chmod +x /build/config/bootstrap.sh
RUN chmod +x /build/config/chroot.sh

# Run the bootstrap script
RUN /build/config/bootstrap.sh

# Build the live image
RUN lb build

# The resulting ISO will be in /build/live-image-amd64.hybrid.iso
