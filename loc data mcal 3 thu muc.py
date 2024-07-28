import os.path
import shutil
import PySimpleGUI as sg

def copy_folders(source_dir, destination_dir):
    # Lấy danh sách tất cả các thư mục trong thư mục nguồn
    for root, dirs, files in os.walk(source_dir):
        # Kiểm tra xem thư mục có 3 thư mục con không
        if len(dirs) == 3:
            # Tạo thư mục đích nếu không tồn tại
            dest_path = os.path.join(destination_dir, os.path.relpath(root, source_dir))
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            
            # Sao chép thư mục con vào thư mục đích
            for directory in dirs:
                shutil.copytree(os.path.join(root, directory), os.path.join(dest_path, directory))
def delete_folders(source_dir):
    # Tạo một từ điển để lưu trữ tên thư mục
    folder_names = {}

    # Lặp qua tất cả các thư mục trong thư mục nguồn
    for root, dirs, files in os.walk(source_dir):
        for directory in dirs:
            folder_name = directory[:20]  # Lấy 20 ký tự đầu của tên thư mục
            if folder_name not in folder_names:
                folder_names[folder_name] = [os.path.join(root, directory)]
            else:
                folder_names[folder_name].append(os.path.join(root, directory))
    
    # Xoá các thư mục có 20 ký tự đầu giống nhau (trừ thư mục đầu tiên)
    for folder_name, folder_paths in folder_names.items():
        if len(folder_paths) > 1:
            for path in folder_paths[1:]:
                print("Deleting folder:", path)
                shutil.rmtree(path)
# Thư mục nguồn và thư mục đích
source_directory = r"D:\data"
destination_directory = r"D:\loc3"

# Gọi hàm để sao chép thư mục
copy_folders(source_directory, destination_directory)
delete_folders(destination_directory)
