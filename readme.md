# **OCI Linux Builder - macOS Guide**

This guide provides step-by-step instructions for macOS users to build a live USB image of "OCI Linux" using Docker and Docker Compose. The instructions focus on setting up the project without including the full contents of the files, ensuring clarity and ease of maintenance.

## **Table of Contents**

1. [Prerequisites](#prerequisites)
2. [Project Directory Structure](#project-directory-structure)
3. [Setting Up the Project Files](#setting-up-the-project-files)
4. [Installing Docker Desktop on macOS](#installing-docker-desktop-on-macos)
5. [Building and Running the Docker Container](#building-and-running-the-docker-container)
6. [Accessing the Output ISO File](#accessing-the-output-iso-file)
7. [Writing the ISO to a USB Drive](#writing-the-iso-to-a-usb-drive)
8. [Troubleshooting and Tips](#troubleshooting-and-tips)
9. [Security Considerations](#security-considerations)
10. [Conclusion](#conclusion)
11. [Next Steps](#next-steps)
12. [Additional Resources](#additional-resources)

---

## **Prerequisites**

Before you begin, ensure you have the following installed on your macOS system:

- **Docker Desktop for Mac**: Includes Docker Engine, Docker CLI client, Docker Compose, and other tools.
- **Git** (optional): For cloning repositories if needed.
- **Homebrew** (optional but recommended): For installing packages on macOS.

---

## **Project Directory Structure**

Create a project directory to hold all necessary files:

```
oci-linux-builder/
├── Dockerfile
├── docker-compose.yml
├── config/
│   ├── bootstrap.sh
│   ├── chroot.sh
│   └── installer.py
└── output/
```

- **Dockerfile**: Defines the Docker image build instructions.
- **docker-compose.yml**: Configures the Docker services.
- **config/**: Contains build scripts and the installer application.
  - **bootstrap.sh**: Sets up the live-build configuration.
  - **chroot.sh**: Customizes the chroot environment during the build.
  - **installer.py**: The GTK+ installer application script.
- **output/**: Directory where the built ISO image will be stored.

---

## **Setting Up the Project Files**

### **1. Clone the Repository (If Available)**

If your project is hosted on a platform like GitHub or GitLab, clone it using:

```bash
git clone https://github.com/yourusername/oci-linux-builder.git
cd oci-linux-builder
```

_Replace `yourusername` with your actual username and ensure the repository is accessible._

### **2. Create the Project Directory Manually (If Not Cloning)**

If you're setting up the project manually:

```bash
mkdir oci-linux-builder
cd oci-linux-builder
mkdir config output
```

### **3. Create the `Dockerfile`**

In the `oci-linux-builder` directory, create a file named `Dockerfile` with the following key components:

- **Base Image**: Use Debian Bullseye.
- **Environment Variable**: Set `DEBIAN_FRONTEND` to `noninteractive`.
- **Install Necessary Packages**: Include `live-build`, `syslinux`, `xorriso`, `cpio`, and Python GTK+ bindings.
- **Set Working Directory**: `/build`
- **Copy Build Scripts**: Copy the `config` directory into the container.
- **Make Scripts Executable**: Use `chmod +x` for `bootstrap.sh` and `chroot.sh`.
- **Run the Bootstrap Script**: Execute `/build/config/bootstrap.sh`.
- **Build the Live Image**: Run `lb build`.

_Note: Ensure all paths and commands are correctly specified in the Dockerfile._

### **4. Create the `docker-compose.yml` File**

In the `oci-linux-builder` directory, create `docker-compose.yml` with the following configurations:

- **Version**: '3.8'
- **Services**:
  - **oci-linux-builder**:
    - **Build Context**: Current directory.
    - **Dockerfile**: Specify the `Dockerfile` created earlier.
    - **Image Name**: `oci-linux-builder:latest`
    - **Container Name**: `oci-linux-builder`
    - **Volumes**:
      - Map `./output` to `/build/output` inside the container.
      - Map `./config` to `/build/config` inside the container.
    - **TTY and STDIN**: Set `tty: true` and `stdin_open: true`.

_Note: Omit `privileged` mode and `network_mode: host` since they are not fully supported on macOS._

### **5. Create the Build Scripts**

#### **a. `config/bootstrap.sh`**

Create `bootstrap.sh` in the `config` directory:

- **Purpose**: Sets up the live-build configuration and includes necessary files.
- **Key Steps**:
  - Install `live-build`.
  - Configure live-build with `lb config` using appropriate options.
  - Copy `installer.py` into the build.
  - Include the `chroot.sh` script as a live-build hook.

#### **b. `config/chroot.sh`**

Create `chroot.sh` in the `config` directory:

- **Purpose**: Customizes the chroot environment during the build process.
- **Key Steps**:
  - Install necessary packages like `xorg`, `xinit`, `openbox`, `python3`, and GTK+ bindings.
  - Create a non-root user (`ociuser`) for running the installer.
  - Copy `installer.py` to the user's home directory.
  - Configure Openbox to autostart the installer.
  - Set up a systemd service to launch the installer on boot.
  - Enable necessary services like `installer.service` and `NetworkManager`.

#### **c. Ensure Scripts Are Executable**

Set executable permissions:

```bash
chmod +x config/bootstrap.sh
chmod +x config/chroot.sh
```

### **6. Create the Installer Application**

Create `installer.py` in the `config` directory:

- **Purpose**: Provides a GTK+ installer application for the user interface.
- **Key Components**:
  - Uses Python 3 and PyGObject (GTK+ bindings).
  - Implements a multi-step wizard for installation steps like language selection, network configuration, and disk setup.
  - Includes methods to handle user input and navigate between steps.

_Note: Since the full code is extensive, refer to your development files for the complete implementation. Ensure `installer.py` has the correct shebang (`#!/usr/bin/env python3`) and executable permissions (`chmod +x config/installer.py`)._

---

## **Installing Docker Desktop on macOS**

### **1. Download Docker Desktop**

- Visit the [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop) download page.
- Download the appropriate version for your macOS.

### **2. Install Docker Desktop**

- Open the downloaded `.dmg` file.
- Drag the Docker icon to the Applications folder.
- Launch Docker Desktop from the Applications folder.
- Follow any on-screen instructions to complete the setup.

### **3. Verify Installation**

In Terminal, run:

```bash
docker --version
docker-compose --version
```

You should see the versions of Docker and Docker Compose installed.

---

## **Building and Running the Docker Container**

### **1. Navigate to Your Project Directory**

```bash
cd path/to/oci-linux-builder
```

### **2. Build and Run the Container Using Docker Compose**

Run:

```bash
docker-compose up --build
```

- The `--build` flag forces a rebuild of the Docker image before starting the container.

### **3. Monitor the Build Process**

- The build process will execute as defined in your Dockerfile and scripts.
- Output will be displayed in the terminal.
- The process may take some time on the first run.

### **4. Check for Completion**

- The build is complete when you see messages indicating the successful completion of `lb build`.
- The Docker container may remain running or exit depending on the final commands.

---

## **Accessing the Output ISO File**

After the build completes, the ISO file will be available in the `output` directory on your host machine.

- **ISO File Location**: `oci-linux-builder/output/live-image-amd64.hybrid.iso`

---

## **Writing the ISO to a USB Drive**

### **1. Insert a USB Drive**

- Connect the USB drive to your Mac.
- **Warning**: This process will erase all data on the USB drive.

### **2. Identify the USB Drive**

List all disk devices:

```bash
diskutil list
```

- Identify your USB drive's device identifier (e.g., `/dev/disk2`).
- **Ensure you have the correct disk identifier to prevent data loss.**

### **3. Unmount the USB Drive**

Replace `/dev/diskN` with your USB drive's identifier:

```bash
diskutil unmountDisk /dev/diskN
```

### **4. Write the ISO to the USB Drive**

Use the `dd` command:

```bash
sudo dd if=output/live-image-amd64.hybrid.iso of=/dev/rdiskN bs=4m
```

- **Example**:

  ```bash
  sudo dd if=output/live-image-amd64.hybrid.iso of=/dev/rdisk2 bs=4m
  ```

- **Notes**:
  - `rdiskN` refers to the raw disk device for faster write speeds.
  - The `bs=4m` sets the block size to 4 megabytes.
  - There is no progress indicator; wait until the command completes.

### **5. Eject the USB Drive**

```bash
diskutil eject /dev/diskN
```

---

## **Troubleshooting and Tips**

### **1. Docker Limitations on macOS**

- **Privileged Mode**: Not fully supported due to Docker running inside a VM on macOS.
- **Network Mode**: `host` network mode is not supported; `bridge` mode is used instead.
- **File Permissions**: Differences may exist between the host and container. Ensure scripts are executable within the container.

### **2. Build Failures**

- **Dependency Issues**: Verify all required packages are specified in the Dockerfile and scripts.
- **Script Errors**: Check syntax and execution permissions for `bootstrap.sh`, `chroot.sh`, and `installer.py`.

### **3. Accessing the Docker Container**

For debugging:

```bash
docker exec -it oci-linux-builder /bin/bash
```

- **Note**: GUI applications won't display on your macOS host due to Docker's VM isolation.

### **4. Testing the Live USB**

- Boot from the USB drive on a compatible PC or use virtualization software.
- macOS may not boot from the USB due to different boot architectures.

### **5. Using a Virtual Machine for Testing**

- Use VirtualBox, VMware Fusion, or Parallels Desktop.
- Create a new VM and attach the ISO file as a virtual CD/DVD drive.

---

## **Security Considerations**

- **Data Loss Risk**: Always double-check disk identifiers when using `dd` to prevent overwriting important data.
- **Script Integrity**: Ensure all scripts are from trusted sources.
- **Permissions**: Avoid running containers with unnecessary privileges.

---

## **Conclusion**

You have now set up the environment to build a live USB image of "OCI Linux" using Docker and Docker Compose on macOS. By following this guide, you can customize and build your own Linux distribution leveraging OCI images.

---

## **Next Steps**

- **Enhance the Installer**: Implement the actual installation logic in your GTK+ installer (`installer.py`).
- **Customize the Build**: Modify the build scripts to include additional packages or configurations as needed.
- **Testing**: Thoroughly test the live USB on various hardware or virtual machines.
- **Collaboration**: Share your project on platforms like GitHub or GitLab to gather feedback and contributions.

---

## **Additional Resources**

- **Docker Desktop for Mac Documentation**: [Docker Docs](https://docs.docker.com/docker-for-mac/)
- **GNU dd Manual**: [dd Manual](https://www.gnu.org/software/coreutils/manual/html_node/dd-invocation.html)
- **Debian Live Build Manual**: [Live Build Manual](https://live-team.pages.debian.net/live-manual/)
- **GTK+ 3 Documentation**: [GTK+ 3 Reference Manual](https://developer.gnome.org/gtk3/stable/)

---

**Feel free to reach out if you have any questions or need further assistance. Happy building!**
