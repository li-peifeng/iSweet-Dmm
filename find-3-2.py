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

def is_3_2_aspect_ratio(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return abs(width / height - 2/3) < 0.01  # 允许微小误差
    except Exception as e:
        print(f"无法检查图片比例: {e}")
        return False

def find_poster_files(directory):
    poster_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower() == "poster.jpg":
                poster_path = os.path.join(root, file)
                if is_3_2_aspect_ratio(poster_path):
                    poster_files.append(poster_path)
    return poster_files

def move_directory(src_path, dest_dir):
    # 获取源目录的基名
    base_name = os.path.basename(src_path)
    # 创建目标路径
    dest_path = os.path.join(dest_dir, base_name)
    
    # 如果目标已存在，添加数字后缀
    counter = 1
    while os.path.exists(dest_path):
        dest_path = os.path.join(dest_dir, f"{base_name}_{counter}")
        counter += 1
    
    # 移动目录
    shutil.move(src_path, dest_path)
    print(f"已移动: {src_path} -> {dest_path}")
    return dest_path

def remove_empty_dirs(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):  # 如果目录为空
                    os.rmdir(dir_path)
                    print(f"已删除空目录: {dir_path}")
            except Exception as e:
                print(f"无法删除目录 {dir_path}: {e}")

def main():
    # 选择操作目录
    source_dir = select_directory("请选择要搜索的目录")
    if not source_dir:
        print("未选择目录，操作取消")
        return
    
    # 查找符合条件的poster.jpg文件
    poster_files = find_poster_files(source_dir)
    if not poster_files:
        print("未找到符合条件的poster.jpg文件")
        return
    
    print(f"找到 {len(poster_files)} 个符合条件的poster.jpg文件:")
    for i, file in enumerate(poster_files, 1):
        print(f"{i}. {file}")
    
    # 选择目标目录
    dest_dir = select_directory("请选择目标目录")
    if not dest_dir:
        print("未选择目标目录，操作取消")
        return
    
    # 移动每个包含poster.jpg的目录
    for poster_path in poster_files:
        src_dir = os.path.dirname(poster_path)
        move_directory(src_dir, dest_dir)
    
    # 递归删除源目录中的空目录
    remove_empty_dirs(source_dir)
    print("操作完成")

if __name__ == "__main__":
    main()