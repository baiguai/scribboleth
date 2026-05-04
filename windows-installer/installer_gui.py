#!/usr/bin/env python3
"""
Scribboleth Installer GUI
A Python tkinter application for installing and uninstalling Scribboleth instances on Windows.
Can be compiled to .exe using PyInstaller: pyinstaller --onefile --windowed installer_gui.py
"""

import os
import sys
import shutil
import subprocess
import re
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, messagebox

class ScribbolethInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Scribboleth Installer")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        self.scrnodes_path = Path.home() / "scrnodes.bat"

        # Get base directory - works both for .py and .exe (PyInstaller)
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller .exe
            self.base_dir = Path(sys.executable).parent
        else:
            # Running as .py script
            self.base_dir = Path(__file__).parent.parent

        self.setup_ui()

    def setup_ui(self):
        # Title
        title = Label(self.root, text="Scribboleth Installer", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both', padx=10, pady=5)

        # Install tab
        install_frame = Frame(notebook)
        notebook.add(install_frame, text="Install")
        self.setup_install_tab(install_frame)

        # Uninstall tab
        uninstall_frame = Frame(notebook)
        notebook.add(uninstall_frame, text="Uninstall")
        self.setup_uninstall_tab(uninstall_frame)

        # Status bar
        self.status_var = StringVar()
        self.status_var.set("Ready")
        status_bar = Label(self.root, textvariable=self.status_var, relief=SUNKEN, anchor=W)
        status_bar.pack(side=BOTTOM, fill=X)

    def setup_install_tab(self, frame):
        Label(frame, text="Install New Scribboleth Instance", font=("Arial", 12)).pack(pady=10)

        # Target path
        path_frame = Frame(frame)
        path_frame.pack(fill='x', padx=20, pady=5)

        Label(path_frame, text="Target HTML File:").pack(anchor='w')
        self.install_path_var = StringVar()
        path_entry = Entry(path_frame, textvariable=self.install_path_var, width=50)
        path_entry.pack(side=LEFT, fill='x', expand=True)

        browse_btn = Button(path_frame, text="Browse", command=self.browse_install_path)
        browse_btn.pack(side=LEFT, padx=5)

        # Port display
        port_frame = Frame(frame)
        port_frame.pack(fill='x', padx=20, pady=5)

        Label(port_frame, text="Assigned Port:").pack(side=LEFT)
        self.port_var = StringVar()
        self.port_var.set("Will be determined automatically")
        Label(port_frame, textvariable=self.port_var, font=("Arial", 10, "bold")).pack(side=LEFT, padx=10)

        # Install button
        install_btn = Button(frame, text="Install", command=self.install, bg="green", fg="white",
                            font=("Arial", 10, "bold"), height=2, width=20)
        install_btn.pack(pady=20)

        # Log area
        Label(frame, text="Log:").pack(anchor='w', padx=20)
        self.install_log = Text(frame, height=10, wrap=WORD)
        self.install_log.pack(fill='both', expand=True, padx=20, pady=5)

    def setup_uninstall_tab(self, frame):
        Label(frame, text="Uninstall Scribboleth Instance", font=("Arial", 12)).pack(pady=10)

        # Target path
        path_frame = Frame(frame)
        path_frame.pack(fill='x', padx=20, pady=5)

        Label(path_frame, text="HTML File to Remove:").pack(anchor='w')
        self.uninstall_path_var = StringVar()
        path_entry = Entry(path_frame, textvariable=self.uninstall_path_var, width=50)
        path_entry.pack(side=LEFT, fill='x', expand=True)

        browse_btn = Button(path_frame, text="Browse", command=self.browse_uninstall_path)
        browse_btn.pack(side=LEFT, padx=5)

        # Uninstall button
        uninstall_btn = Button(frame, text="Uninstall", command=self.uninstall, bg="red", fg="white",
                              font=("Arial", 10, "bold"), height=2, width=20)
        uninstall_btn.pack(pady=20)

        # Log area
        Label(frame, text="Log:").pack(anchor='w', padx=20)
        self.uninstall_log = Text(frame, height=10, wrap=WORD)
        self.uninstall_log.pack(fill='both', expand=True, padx=20, pady=5)

    def browse_install_path(self):
        filename = filedialog.asksaveasfilename(
            title="Select target HTML file location",
            filetypes=[("HTML files", "*.html")],
            defaultextension=".html"
        )
        if filename:
            self.install_path_var.set(filename)

    def browse_uninstall_path(self):
        filename = filedialog.askopenfilename(
            title="Select HTML file to uninstall",
            filetypes=[("HTML files", "*.html")]
        )
        if filename:
            self.uninstall_path_var.set(filename)

    def log_install(self, message):
        self.install_log.insert(END, message + "\n")
        self.install_log.see(END)
        self.root.update_idletasks()

    def log_uninstall(self, message):
        self.uninstall_log.insert(END, message + "\n")
        self.uninstall_log.see(END)
        self.root.update_idletasks()

    def get_next_port(self):
        """Get the next available port from scrnodes.bat"""
        if not self.scrnodes_path.exists():
            return 3000

        ports = []
        content = self.scrnodes_path.read_text(errors='ignore')

        # Find REM port lines
        rem_ports = re.findall(r'^REM\s+(\d+)', content, re.MULTILINE)
        ports.extend([int(p) for p in rem_ports])

        # Find echo port lines
        echo_ports = re.findall(r'echo\s+\S+:\s*(\d+)', content)
        ports.extend([int(p) for p in echo_ports])

        if ports:
            return max(ports) + 1
        return 3000

    def install(self):
        target_path = self.install_path_var.get().strip()
        if not target_path:
            messagebox.showerror("Error", "Please select a target HTML file path")
            return

        target_path = Path(target_path)
        target_dir = target_path.parent
        filename = target_path.stem

        html_file = target_dir / f"{filename}.html"
        saver_file = target_dir / f"svr_{filename}.js"

        # Check if already exists
        if html_file.exists() and saver_file.exists():
            messagebox.showerror("Error", f"Installation for {filename} already exists")
            return

        self.log_install(f"Installing {filename} in {target_dir}")

        # Determine port
        port = self.get_next_port()
        self.port_var.set(str(port))
        self.log_install(f"Using port {port}")

        try:
            # Check for Node.js and npm
            self.log_install("Checking for Node.js and npm...")
            try:
                subprocess.run("node --version", shell=True, check=True, capture_output=True)
                subprocess.run("npm --version", shell=True, check=True, capture_output=True)
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Node.js or npm is not installed.\nPlease install Node.js from https://nodejs.org/")
                return
            self.log_install("Node.js and npm found")

            # Create target directory
            target_dir.mkdir(parents=True, exist_ok=True)

            # Copy and modify HTML file
            src_html = self.base_dir / "scribboleth.html"
            if not src_html.exists():
                messagebox.showerror("Error", f"scribboleth.html not found in {self.base_dir}")
                return

            html_content = src_html.read_text()
            html_content = re.sub(r'let nodePort = \d+;', f'let nodePort = {port};', html_content)
            html_content = re.sub(r'let fileName = ".*?";', f'let fileName = "{filename}";', html_content)
            html_file.write_text(html_content)
            self.log_install(f"Created {html_file}")

            # Copy and modify saver.js
            src_saver = self.base_dir / "saver.js"
            if not src_saver.exists():
                messagebox.showerror("Error", f"saver.js not found in {self.base_dir}")
                return

            saver_content = src_saver.read_text()
            saver_content = re.sub(r'const FILE_PATH = ".*?";', f'const FILE_PATH = "./{filename}.html";', saver_content)
            saver_content = re.sub(r'const PORT = \d+;', f'const PORT = {port};', saver_content)
            saver_file.write_text(saver_content)
            self.log_install(f"Created {saver_file}")

            # Update scrnodes.bat
            self.update_scrnodes(target_dir, saver_file, filename, port)

            # Create package.json and install npm packages
            self.log_install("Installing npm dependencies...")
            package_json = target_dir / "package.json"
            package_json.write_text('{ "type": "module", "dependencies": { "express": "^5.1.0", "body-parser": "^1.20.0" } }')

            # Run npm install
            result = subprocess.run("npm install", shell=True, cwd=str(target_dir),
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.log_install("npm install completed successfully")
            else:
                self.log_install(f"npm install warning: {result.stderr}")

            self.log_install(f"Installation complete! Port: {port}")
            self.log_install(f"Run {self.scrnodes_path} to start the service")
            messagebox.showinfo("Success", f"Scribboleth instance '{filename}' installed on port {port}")

        except Exception as e:
            self.log_install(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))

    def update_scrnodes(self, target_dir, saver_file, filename, port):
        """Update or create scrnodes.bat"""
        if self.scrnodes_path.exists():
            self.log_install("Updating existing scrnodes.bat...")

            # Check if instance already exists
            content = self.scrnodes_path.read_text(errors='ignore')
            if str(saver_file) in content:
                self.log_install("Instance already exists in scrnodes.bat")
                return

            # Read existing content
            lines = content.split('\n')

            # Find last REM port line and add new one
            last_rem_idx = -1
            for i, line in enumerate(lines):
                if re.match(r'^REM\s+\d+', line.strip()):
                    last_rem_idx = i

            if last_rem_idx >= 0:
                lines.insert(last_rem_idx + 1, f"REM {port}")

            # Find :wait_loop and insert before it
            wait_loop_idx = -1
            for i, line in enumerate(lines):
                if ':wait_loop' in line:
                    wait_loop_idx = i
                    break

            if wait_loop_idx >= 0:
                # Adjust for inserted REM line
                if last_rem_idx >= 0 and last_rem_idx < wait_loop_idx:
                    wait_loop_idx += 1

                lines.insert(wait_loop_idx, f'cd /d "{target_dir}"')
                lines.insert(wait_loop_idx + 1, f'start "" /b cmd /c "node "{saver_file}" >nul 2>&1"')
                wait_loop_idx += 2

            # Find last echo line and add new one
            last_echo_idx = -1
            for i in range(min(wait_loop_idx, len(lines))):
                if re.search(r'echo\s+\S+:\s*\d+', lines[i]):
                    last_echo_idx = i

            if last_echo_idx >= 0:
                # Remove extra blank echo lines before adding new one
                if last_echo_idx + 1 < len(lines) and lines[last_echo_idx + 1].strip() == 'echo.':
                    # Remove consecutive echo. lines
                    while last_echo_idx + 1 < len(lines) and lines[last_echo_idx + 1].strip() == 'echo.':
                        lines.pop(last_echo_idx + 1)
                lines.insert(last_echo_idx + 1, f'echo {filename}: {port}')
                lines.insert(last_echo_idx + 2, 'echo.')

            self.scrnodes_path.write_text('\n'.join(lines), encoding='ascii')
            self.log_install("Updated scrnodes.bat")

        else:
            self.log_install("Creating new scrnodes.bat...")
            # Escape backslashes for batch file
            target_dir_bat = str(target_dir).replace('\\', '\\\\')
            saver_file_bat = str(saver_file).replace('\\', '\\\\')
            content = f"""@echo off
REM {port}

cd /d "{target_dir}"
start "" /b cmd /c "node \\"{saver_file_bat}\\" >nul 2>&1"

timeout /t 3 /nobreak >nul

echo {filename}: {port}

:wait_loop
timeout /t 1 /nobreak >nul
goto wait_loop
"""
            self.scrnodes_path.write_text(content, encoding='ascii')
            self.log_install("Created scrnodes.bat")

    def uninstall(self):
        target_path = self.uninstall_path_var.get().strip()
        if not target_path:
            messagebox.showerror("Error", "Please select an HTML file to uninstall")
            return

        target_path = Path(target_path)
        target_dir = target_path.parent
        filename = target_path.stem

        html_file = target_dir / f"{filename}.html"
        saver_file = target_dir / f"svr_{filename}.js"

        if not html_file.exists():
            messagebox.showerror("Error", f"{html_file} not found")
            return

        # Get port from HTML file
        try:
            html_content = html_file.read_text()
            port_match = re.search(r'let nodePort = (\d+);', html_content)
            port = port_match.group(1) if port_match else None
        except:
            port = None

        # Confirm
        if not messagebox.askyesno("Confirm", f"Uninstall {filename} from {target_dir}?"):
            return

        self.log_uninstall(f"Uninstalling {filename}...")

        try:
            # Remove files
            if html_file.exists():
                html_file.unlink()
                self.log_uninstall(f"Removed {html_file}")

            if saver_file.exists():
                saver_file.unlink()
                self.log_uninstall(f"Removed {saver_file}")

            # Remove package.json
            package_json = target_dir / "package.json"
            if package_json.exists():
                package_json.unlink()
                self.log_uninstall(f"Removed {package_json}")

            # Clean scrnodes.bat
            if self.scrnodes_path.exists():
                self.clean_scrnodes(filename, port, str(saver_file), target_dir)

            self.log_uninstall("Uninstallation complete!")
            messagebox.showinfo("Success", f"Scribboleth instance '{filename}' uninstalled")

        except Exception as e:
            self.log_uninstall(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))

    def clean_scrnodes(self, filename, port, saver_file, target_dir):
        """Remove instance from scrnodes.bat"""
        self.log_uninstall("Cleaning scrnodes.bat...")

        content = self.scrnodes_path.read_text(errors='ignore')
        lines = content.split('\n')

        # Remove lines related to this instance
        new_lines = []
        skip_next = False

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # Skip REM port line
            if port and line_stripped == f"REM {port}":
                continue

            # Skip cd line for this instance
            if f'cd /d "{target_dir}"' in line or f'cd /d "{target_dir}"' in line:
                # Check if next line is the start line
                if i + 1 < len(lines) and 'start' in lines[i+1] and str(saver_file) in lines[i+1]:
                    skip_next = True
                continue

            # Skip start line for this instance
            if skip_next and str(saver_file) in line:
                skip_next = False
                continue
            elif skip_next:
                skip_next = False

            # Skip echo line for this instance
            if port and f'echo {filename}: {port}' in line:
                continue

            new_lines.append(line)

        # Remove empty lines but keep structure
        # First pass: remove consecutive blank lines
        cleaned = []
        prev_blank = False
        for line in new_lines:
            is_blank = line.strip() == ''
            if not is_blank or not prev_blank:
                cleaned.append(line)
            prev_blank = is_blank

        self.scrnodes_path.write_text('\n'.join(cleaned), encoding='ascii')
        self.log_uninstall("scrnodes.bat cleaned")


if __name__ == "__main__":
    root = Tk()
    app = ScribbolethInstaller(root)
    root.mainloop()
