import os
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image

def select_directory(title):
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title=title)
    return directory

def find_poster_jpg(directory):
    poster_files = []
    for root, _, files in os.walk(directory):
        if 'poster.jpg' in files:
            poster_path = os.path.join(root, 'poster.jpg')
            poster_files.append(poster_path)
    return poster_files

def check_resolution(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        return height > 540  # 修改为 <= 540

def move_directory(src_path, dest_dir):
    # 获取源目录和目录名
    src_dir = os.path.dirname(src_path)
    dir_name = os.path.basename(src_dir)
    
    # 检查源目录是否存在
    if not os.path.exists(src_dir):
        print(f"警告: 源目录已不存在 {src_dir}")
        return
    
    # 创建目标路径
    dest_path = os.path.join(dest_dir, dir_name)
    
    try:
        # 如果目标路径已存在，先删除
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
        
        # 移动整个目录
        shutil.move(src_dir, dest_dir)
        print(f"成功移动: {src_dir} -> {dest_path}")
        
        # 检查并删除空目录（包括上级目录）
        parent_dir = os.path.dirname(src_dir)
        while parent_dir != source_directory:
            if os.path.exists(parent_dir) and not os.listdir(parent_dir):
                try:
                    os.rmdir(parent_dir)
                    print(f"删除空目录: {parent_dir}")
                    parent_dir = os.path.dirname(parent_dir)  # 继续检查上一级
                except OSError as e:
                    print(f"无法删除目录 {parent_dir}: {str(e)}")
                    break
            else:
                break  # 目录不为空，停止检查
                
    except Exception as e:
        print(f"移动 {src_dir} 时出错: {str(e)}")
        raise

def main():
    global source_directory
    
    # Step 1: Select source directory
    source_directory = select_directory("选择要搜索的目录")
    if not source_directory:
        print("未选择目录，程序退出")
        return
    
    # Step 2: Find all poster.jpg files
    poster_files = find_poster_jpg(source_directory)
    if not poster_files:
        print("未找到 poster.jpg 文件")
        return
    
    # Step 3: Check resolution and collect files to move
    low_res_files = [f for f in poster_files if check_resolution(f)]
    if not low_res_files:
        print("所有 poster.jpg 文件分辨率都小于540px")
        return
    
    print(f"找到 {len(low_res_files)} 个分辨率高于540px的poster.jpg文件")
    
    # Step 4: Select destination directory
    dest_directory = select_directory("选择目标文件夹")
    if not dest_directory:
        print("未选择目标文件夹，程序退出")
        return
    
    # Step 5: Move directories
    for file_path in low_res_files:
        try:
            move_directory(file_path, dest_directory)
            print(f"已移动: {file_path}")
        except Exception as e:
            print(f"移动 {file_path} 时出错: {str(e)}")
    
    print("操作完成")

if __name__ == "__main__":
    main()