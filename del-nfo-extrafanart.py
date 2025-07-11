import os
import tkinter as tk
from tkinter import filedialog
import shutil

def delete_nfo_files_and_extrafanart_folders(root_dir):
    deleted_nfo_count = 0
    deleted_extrafanart_count = 0
    
    for root, dirs, files in os.walk(root_dir, topdown=False):
        # 删除.nfo文件
        for file in files:
            if file.lower().endswith('.nfo'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"已删除文件: {file_path}")
                    deleted_nfo_count += 1
                except Exception as e:
                    print(f"删除文件失败 {file_path}: {e}")
        
        # 删除extrafanart文件夹
        for dir_name in dirs:
            if dir_name.lower() == 'extrafanart':
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"已删除文件夹: {dir_path}")
                    deleted_extrafanart_count += 1
                except Exception as e:
                    print(f"删除文件夹失败 {dir_path}: {e}")
    
    print(f"\n操作完成！")
    print(f"共删除 {deleted_nfo_count} 个.nfo文件")
    print(f"共删除 {deleted_extrafanart_count} 个extrafanart文件夹")

def select_directory():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    # 选择目录
    folder_selected = filedialog.askdirectory(title="请选择要处理的目录")
    
    if folder_selected:
        print(f"您选择的目录是: {folder_selected}")
        confirm = input("确定要删除此目录及其子目录下的所有.nfo文件和extrafanart文件夹吗？(y/n): ")
        if confirm.lower() == 'y':
            delete_nfo_files_and_extrafanart_folders(folder_selected)
        else:
            print("操作已取消")
    else:
        print("未选择目录，程序退出")

if __name__ == "__main__":
    select_directory()
    input("按Enter键退出...")