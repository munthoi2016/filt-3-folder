import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def copy_matching_files_and_folders(source_dir, dest_dir, num_chars, prefix, progress_var):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    items = os.listdir(source_dir)
    name_dict = {}

    for item in items:
        item_path = os.path.join(source_dir, item)

        if item.startswith(prefix):
            name_key = item[len(prefix):len(prefix) + num_chars]  # Bỏ qua prefix và lấy num_chars ký tự sau đó
        else:
            name_key = item[:num_chars]  # Lấy num_chars ký tự đầu tiên

        if name_key not in name_dict:
            name_dict[name_key] = []

        name_dict[name_key].append(item_path)

    total_items = sum(len(paths) for paths in name_dict.values())
    processed_items = 0

    for name_key, paths in name_dict.items():
        if len(paths) > 1:
            for path in paths:
                if os.path.isdir(path):
                    shutil.copytree(path, os.path.join(dest_dir, os.path.basename(path)))
                else:
                    shutil.copy2(path, os.path.join(dest_dir, os.path.basename(path)))
                processed_items += 1
                progress_var.set((processed_items / total_items) * 100)
                root.update_idletasks()

    messagebox.showinfo("Thành công", "Đã sao chép các tệp và thư mục thành công!")

def select_source_dir():
    source_dir = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_dir)

def select_dest_dir():
    dest_dir = filedialog.askdirectory()
    dest_entry.delete(0, tk.END)
    dest_entry.insert(0, dest_dir)

def start_copy():
    source_dir = source_entry.get()
    dest_dir = dest_entry.get()
    try:
        num_chars = int(num_chars_entry.get())
    except ValueError:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập một số hợp lệ cho số ký tự.")
        return

    prefix = prefix_entry.get()

    if not source_dir or not dest_dir:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn cả thư mục nguồn và thư mục đích.")
        return

    progress_var.set(0)
    copy_matching_files_and_folders(source_dir, dest_dir, num_chars, prefix, progress_var)

# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Sao chép tệp và thư mục")

# Thư mục nguồn
source_label = tk.Label(root, text="Thư mục nguồn:")
source_label.grid(row=0, column=0, padx=10, pady=10)
source_entry = tk.Entry(root, width=50)
source_entry.grid(row=0, column=1, padx=10, pady=10)
source_button = tk.Button(root, text="Chọn...", command=select_source_dir)
source_button.grid(row=0, column=2, padx=10, pady=10)

# Thư mục đích
dest_label = tk.Label(root, text="Thư mục đích:")
dest_label.grid(row=1, column=0, padx=10, pady=10)
dest_entry = tk.Entry(root, width=50)
dest_entry.grid(row=1, column=1, padx=10, pady=10)
dest_button = tk.Button(root, text="Chọn...", command=select_dest_dir)
dest_button.grid(row=1, column=2, padx=10, pady=10)

# Số ký tự trùng nhau
num_chars_label = tk.Label(root, text="Số ký tự trùng nhau:")
num_chars_label.grid(row=2, column=0, padx=10, pady=10)
num_chars_entry = tk.Entry(root, width=10)
num_chars_entry.grid(row=2, column=1, padx=10, pady=10)
num_chars_entry.insert(0, "20")  # Giá trị mặc định

# Tiền tố
prefix_label = tk.Label(root, text="Tiền tố:")
prefix_label.grid(row=3, column=0, padx=10, pady=10)
prefix_entry = tk.Entry(root, width=10)
prefix_entry.grid(row=3, column=1, padx=10, pady=10)
prefix_entry.insert(0, "F_")  # Giá trị mặc định

# Thanh tiến trình
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=20, sticky='ew')

# Nút bắt đầu sao chép
start_button = tk.Button(root, text="Bắt đầu sao chép", command=start_copy)
start_button.grid(row=5, column=1, padx=10, pady=20)

# Chạy giao diện
root.mainloop()
