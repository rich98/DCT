# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Author: Richard Wadsworth
# Date: May 2025

import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import os
import tempfile

def test_disk_write(path, block_size_mb=100, max_write_gb=None, cleanup=True, log_callback=None):
    """
    Function to write test blocks to the given path to verify actual writable space.
    - path: target directory
    - block_size_mb: size of each test block in MB
    - max_write_gb: limit of data to write, in GB (optional)
    - cleanup: whether to remove test files after writing
    - log_callback: function to receive logging output
    """
    block_size = block_size_mb * 1024 * 1024  # Convert MB to bytes
    max_blocks = float('inf') if not max_write_gb else (max_write_gb * 1024) // block_size_mb
    temp_dir = tempfile.mkdtemp(dir=path)  # Create temp folder on target drive
    if log_callback:
        log_callback(f"[INFO] Temporary directory: {temp_dir}")

    written_blocks = 0
    try:
        while written_blocks < max_blocks:
            file_path = os.path.join(temp_dir, f"test_block_{written_blocks}.bin")
            try:
                with open(file_path, 'wb') as f:
                    f.write(os.urandom(block_size))  # Write random data
                written_blocks += 1
                if log_callback:
                    log_callback(f"[INFO] Wrote block {written_blocks} of size {block_size_mb} MB")
            except OSError as e:
                log_callback(f"[ERROR] Write failed at block {written_blocks}: {e}")
                break

        total_written_gb = (written_blocks * block_size_mb) / 1024
        log_callback(f"[RESULT] Total written: {total_written_gb:.2f} GB in {written_blocks} blocks")
    finally:
        if cleanup:
            log_callback("[INFO] Cleaning up test files...")
            for f in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, f))
            os.rmdir(temp_dir)
            log_callback("[INFO] Cleanup complete.")

class DiskTestApp:
    """
    GUI class for launching the disk write test.
    """
    def __init__(self, root):
        self.root = root
        root.title("Disk Capacity Test")
        root.configure(bg="#2b2b2b")
        root.geometry("400x300")

        # Variables to hold user inputs
        self.dir_var = tk.StringVar()
        self.block_size_var = tk.StringVar(value="100")
        self.limit_var = tk.StringVar()

        # Title label
        tk.Label(root, text="DISK CAPACITY TEST", font=("Helvetica", 16, "bold"), fg="white", bg="#2b2b2b").pack(pady=10)

        # Input fields
        self.create_field("Target Directory:", self.dir_var, browse=True)
        self.create_field("Block Size (MB):", self.block_size_var)
        self.create_field("Limit Write (GB):", self.limit_var)

        # Start button
        self.start_btn = tk.Button(root, text="Start Test", command=self.start_test, font=("Helvetica", 12),
                                   bg="#4b4b4b", fg="white")
        self.start_btn.pack(pady=15)

        # Log output area
        self.log_box = tk.Text(root, height=6, bg="#1e1e1e", fg="lightgrey", font=("Courier", 9))
        self.log_box.pack(fill=tk.BOTH, expand=True)

    def create_field(self, label, variable, browse=False):
        """
        Helper to create a labeled entry field, optionally with directory browser.
        """
        frame = tk.Frame(self.root, bg="#2b2b2b")
        frame.pack(pady=5)
        tk.Label(frame, text=label, width=15, anchor='w', fg="white", bg="#2b2b2b").pack(side=tk.LEFT)
        entry = tk.Entry(frame, textvariable=variable, width=25)
        entry.pack(side=tk.LEFT, padx=5)
        if browse:
            tk.Button(frame, text="...", command=self.browse_directory, width=3).pack(side=tk.LEFT)

    def browse_directory(self):
        """
        Open directory browser and set selection to path entry.
        """
        path = filedialog.askdirectory()
        if path:
            self.dir_var.set(path)

    def log(self, message):
        """
        Append a message to the log output.
        """
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    def start_test(self):
        """
        Validate inputs and run test in a background thread.
        """
        path = self.dir_var.get()
        try:
            block_size = int(self.block_size_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid block size")
            return

        try:
            max_write = int(self.limit_var.get()) if self.limit_var.get() else None
        except ValueError:
            messagebox.showerror("Error", "Invalid GB limit")
            return

        if not os.path.isdir(path):
            messagebox.showerror("Error", "Target directory is invalid")
            return

        self.start_btn.config(state=tk.DISABLED)
        self.log_box.delete(1.0, tk.END)

        def run_test():
            test_disk_write(
                path=path,
                block_size_mb=block_size,
                max_write_gb=max_write,
                cleanup=True,
                log_callback=self.log
            )
            self.start_btn.config(state=tk.NORMAL)

        threading.Thread(target=run_test).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskTestApp(root)
    root.mainloop()

# End of file
# Licensed under the Apache License, Version 2.0
# See: http://www.apache.org/licenses/LICENSE-2.0
