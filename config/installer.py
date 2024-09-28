#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class InstallerWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="OCI Linux Installer")
        self.set_border_width(10)
        self.set_default_size(600, 400)
        self.current_step = 0
        self.steps = [self.page_welcome, self.page_language, self.page_network,
                      self.page_timezone, self.page_kernel, self.page_oci_config,
                      self.page_disk_setup, self.page_user_creation, self.page_installation]

        self.vbox = Gtk.VBox(spacing=6)
        self.add(self.vbox)

        self.content_area = Gtk.Box()
        self.vbox.pack_start(self.content_area, True, True, 0)

        self.navigation_box = Gtk.Box(spacing=6)
        self.vbox.pack_start(self.navigation_box, False, False, 0)

        self.back_button = Gtk.Button(label="Back")
        self.back_button.connect("clicked", self.on_back_clicked)
        self.navigation_box.pack_start(self.back_button, False, False, 0)

        self.next_button = Gtk.Button(label="Next")
        self.next_button.connect("clicked", self.on_next_clicked)
        self.navigation_box.pack_end(self.next_button, False, False, 0)

        self.show_current_step()

    def show_current_step(self):
        for widget in self.content_area.get_children():
            self.content_area.remove(widget)
        self.steps[self.current_step]()
        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        self.back_button.set_sensitive(self.current_step > 0)
        if self.current_step == len(self.steps) - 1:
            self.next_button.set_label("Finish")
        else:
            self.next_button.set_label("Next")

    def on_back_clicked(self, widget):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_current_step()

    def on_next_clicked(self, widget):
        if self.current_step < len(self.steps) - 1:
            if self.validate_step():
                self.current_step += 1
                self.show_current_step()
        else:
            # Finish installation
            Gtk.main_quit()

    def validate_step(self):
        # Add validation logic for each step if necessary
        return True

    # Define each page as a method
    def page_welcome(self):
        label = Gtk.Label(label="Welcome to OCI Linux Installer.\n\nThis installer will guide you through the installation process.")
        self.content_area.pack_start(label, True, True, 0)
        self.content_area.show_all()

    def page_language(self):
        label = Gtk.Label(label="Select Your Language")
        self.language_combo = Gtk.ComboBoxText()
        self.language_combo.append_text("English")
        self.language_combo.append_text("Español")
        self.language_combo.append_text("Français")
        self.language_combo.append_text("Deutsch")
        self.language_combo.append_text("中文")
        self.language_combo.set_active(0)
        vbox = Gtk.VBox(spacing=6)
        vbox.pack_start(label, False, False, 0)
        vbox.pack_start(self.language_combo, False, False, 0)
        self.content_area.pack_start(vbox, True, True, 0)
        self.content_area.show_all()

    def page_network(self):
        label = Gtk.Label(label="Network Configuration")
        # Implement Wi-Fi and Ethernet configuration widgets
        vbox = Gtk.VBox(spacing=6)
        vbox.pack_start(label, False, False, 0)
        # Add more widgets here...
        self.content_area.pack_start(vbox, True, True, 0)
        self.content_area.show_all()

    def page_timezone(self):
        label = Gtk.Label(label="Select Your Time Zone")
        self.timezone_combo = Gtk.ComboBoxText()
        self.timezone_combo.append_text("UTC")
        self.timezone_combo.append_text("America/New_York")
        self.timezone_combo.append_text("Europe/London")
        self.timezone_combo.append_text("Asia/Tokyo")
        self.timezone_combo.append_text("Australia/Sydney")
        self.timezone_combo.set_active(0)
        vbox = Gtk.VBox(spacing=6)
        vbox.pack_start(label, False, False, 0)
        vbox.pack_start(self.timezone_combo, False, False, 0)
        self.content_area.pack_start(vbox, True, True, 0)
        self.content_area.show_all()

    def page_kernel(self):
        label = Gtk.Label(label="Select Linux Kernel Version")
        self.kernel_combo = Gtk.ComboBoxText()
        self.kernel_combo.append_text("5.10")
        self.kernel_combo.append_text("5.15")
        self.kernel_combo.append_text("5.19")
        self.kernel_combo.append_text("6.0")
        self.kernel_combo.append_text("6.1")
        self.kernel_combo.set_active(0)
        vbox = Gtk.VBox(spacing=6)
        vbox.pack_start(label, False, False, 0)
        vbox.pack_start(self.kernel_combo, False, False, 0)
        self.content_area.pack_start(vbox, True, True, 0)
        self.content_area.show_all()

    def page_oci_config(self):
        label = Gtk.Label(label="OCI Configuration")
        self.repo_entry = Gtk.Entry()
        self.repo_entry.set_placeholder_text("Repository (default: docker.io)")
        self.image_entry = Gtk.Entry()
        self.image_entry.set_placeholder_text("Image Name (e.g., ubuntu:latest)")
        self.commands_textview = Gtk.TextView()
        self.commands_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.commands_textview.get_buffer().set_text("Additional Dockerfile Commands")
        vbox = Gtk.VBox(spacing=6)
        vbox.pack_start(label, False, False, 0)
        vbox.pack_start(self.repo_entry, False, False, 0)
        vbox.pack_start(self.image_entry, False, False, 0)
        vbox.pack_start(self.commands_textview, True, True, 0)
        self.content_area.pack_start(vbox, True, True, 0)
        self.content_area.show_all()

    def page_disk_setup(self):
        label = Gtk.Label(label="Disk Setup")
        self.install_type_combo = Gtk.ComboBoxText()
        self.install_type_combo.append_text("Erase disk and install OCI Linux")
        self.install_type_combo.append_text("Install alongside existing OS")
        self.install_type_combo.append_text("Custom partitioning")
        self.install_type_combo.set_active(0)
        self.disk_size_entry = Gtk.Entry()
        self.disk_size_entry.set_placeholder_text("Disk Size (GB)")
        self.swap_size_entry = Gtk.Entry()
        self.swap_size_entry.set_placeholder_text("Swap Size (GB)")
        self.encrypt_checkbox = Gtk.CheckButton(label="Encrypt the new installation")
        vbox = Gtk.VBox(spacing=6)
        vbox.pack_start(label, False, False, 0)
        vbox.pack_start(self.install_type_combo, False, False, 0)
        vbox.pack_start(self.disk_size_entry, False, False, 0)
        vbox.pack_start(self.swap_size_entry, False, False, 0)
        vbox.pack_start(self.encrypt_checkbox, False, False, 0)
        self.content_area.pack_start(vbox, True, True, 0)
        self.content_area.show_all()

    def page_user_creation(self):
        label = Gtk.Label(label="Create Your User Account")
        self.fullname_entry = Gtk.Entry()
        self.fullname_entry.set_placeholder_text("Your Name")
        self.computername_entry = Gtk.Entry()
        self.computername_entry.set_placeholder_text("Computer Name")
        self.username_entry = Gtk.Entry()
        self.username_entry.set_placeholder_text("Username")
        self.password_entry = Gtk.Entry()
        self.password_entry.set_placeholder_text("Password")
        self.password_entry.set_visibility(False)
        self.confirm_password_entry = Gtk.Entry()
        self.confirm_password_entry.set_placeholder_text("Confirm Password")
        self.confirm_password_entry.set_visibility(False)
        self.autologin_checkbox = Gtk.CheckButton(label="Log in automatically without asking for password")
        vbox = Gtk.VBox(spacing=6)
        vbox.pack_start(label, False, False, 0)
        vbox.pack_start(self.fullname_entry, False, False, 0)
        vbox.pack_start(self.computername_entry, False, False, 0)
        vbox.pack_start(self.username_entry, False, False, 0)
        vbox.pack_start(self.password_entry, False, False, 0)
        vbox.pack_start(self.confirm_password_entry, False, False, 0)
        vbox.pack_start(self.autologin_checkbox, False, False, 0)
        self.content_area.pack_start(vbox, True, True, 0)
        self.content_area.show_all()

    def page_installation(self):
        label = Gtk.Label(label="Installing OCI Linux...\nPlease wait while the installation completes.")
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_show_text(True)
        vbox = Gtk.VBox(spacing=6)
        vbox.pack_start(label, False, False, 0)
        vbox.pack_start(self.progress_bar, False, False, 0)
        self.content_area.pack_start(vbox, True, True, 0)
        self.content_area.show_all()
        # Start installation process
        self.start_installation()

    def start_installation(self):
        # Simulate installation progress
        import threading
        import time

        def progress():
            for i in range(101):
                time.sleep(0.1)
                Gtk.idle_add(self.progress_bar.set_fraction, i/100.0)
                Gtk.idle_add(self.progress_bar.set_text, f"{i}%")
            Gtk.idle_add(self.next_button.set_label, "Finish")

        threading.Thread(target=progress).start()

if __name__ == "__main__":
    win = InstallerWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
