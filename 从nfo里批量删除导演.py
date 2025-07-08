# 此脚本用于删除 nfo 文件里的导演标签

import os
import re
import tkinter as tk
from tkinter import filedialog

def select_directory():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    folder_path = filedialog.askdirectory(title="选择要扫描的文件夹")
    return folder_path

def process_nfo_files(folder_path):
    director_pattern = re.compile(r'^\s*<director>.*?</director>\s*?\n', re.MULTILINE)
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.nfo'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 删除director标签行
                    new_content = director_pattern.sub('', content)
                    
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"已处理: {file_path}")
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")

if __name__ == "__main__":
    print("请选择要扫描的文件夹...")
    selected_path = select_directory()
    
    if selected_path:
        print(f"开始处理文件夹: {selected_path}")
        process_nfo_files(selected_path)
        print("处理完成!")
    else:
        print("未选择文件夹，程序退出。")