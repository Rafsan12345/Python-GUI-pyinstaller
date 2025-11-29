import http.server
import socketserver
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

PORT = 8000
server_thread = None
httpd = None

def start_server():
    global server_thread, httpd

    folder = folder_path.get()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Error", "Please select a valid folder!")
        return

    os.chdir(folder)

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)

    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    log_box.insert(tk.END, f"Server started at: http://localhost:{PORT}\n")
    log_box.insert(tk.END, f"Serving folder: {folder}\n\n")

def stop_server():
    global httpd

    if httpd:
        httpd.shutdown()
        httpd = None
        log_box.insert(tk.END, "Server stopped.\n\n")
    else:
        messagebox.showinfo("Info", "Server is not running.")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

# GUI setup
root = tk.Tk()
root.title("Local Server GUI (Port 8000)")
root.geometry("500x350")

folder_path = tk.StringVar()

tk.Label(root, text="Select Folder to Serve:").pack()

tk.Entry(root, textvariable=folder_path, width=50).pack(pady=5)
tk.Button(root, text="Browse", command=browse_folder).pack()

tk.Button(root, text="Start Server", command=start_server, bg="green", fg="white").pack(pady=10)
tk.Button(root, text="Stop Server", command=stop_server, bg="red", fg="white").pack()

log_box = scrolledtext.ScrolledText(root, width=60, height=10)
log_box.pack(pady=10)

root.mainloop()
