# 此脚本用于查找低分辨率poster图片，并在输出目录里生成相同文件夹结构的strm文件，用于刮削高清图使用

import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image

def find_small_posters(root_dir):
    """递归查找所有分辨率高度小于540px的poster.jpg图片，并返回包含路径和分辨率的列表"""
    small_posters = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'poster.jpg' in filenames:
            poster_path = os.path.join(dirpath, 'poster.jpg')
            try:
                with Image.open(poster_path) as img:
                    width, height = img.size
                    if height < 540:
                        small_posters.append((poster_path, width, height))
            except Exception as e:
                print(f"无法处理图片 {poster_path}: {e}")
    return small_posters

def find_large_video_files(directory):
    """查找目录下体积大于300MB的视频文件，按名称排序后返回第一个"""
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.iso', '.rmvb']  # 常见视频扩展名
    video_files = []
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext in video_extensions:
                file_size = os.path.getsize(file_path)  # 文件大小(字节)
                if file_size > 300 * 1024 * 1024:  # 大于300MB
                    video_files.append(file_path)
    
    # 按文件名排序
    video_files.sort()
    
    # 返回第一个匹配的视频文件，如果没有则返回None
    return video_files[0] if video_files else None

def create_strm_files(small_posters, root_dir):
    """为找到的小海报创建strm文件，指向同目录下的大于300MB的视频文件"""
    # 初始化输出目录为None，等待第一次找到符合条件的文件时选择
    output_base_dir = None
    strm_file_paths = []  # 用于存储所有生成的strm文件路径
    
    for poster_path, width, height in small_posters:
        # 如果还没有选择输出目录，则在选择第一个符合条件的文件时弹出对话框
        if output_base_dir is None:
            # 弹出对话框让用户选择输出目录
            print("请为strm文件选择输出目录...")
            output_base_dir = filedialog.askdirectory(title="选择strm文件输出目录")
            
            if not output_base_dir:
                print("未选择输出目录，程序退出")
                exit(1)
            
            # 确保输出目录存在
            if not os.path.exists(output_base_dir):
                os.makedirs(output_base_dir)
        
        # 获取海报所在目录
        poster_dir = os.path.dirname(poster_path)
        
        # 查找同目录下的大于300MB的视频文件
        video_file = find_large_video_files(poster_dir)
        
        if video_file:
            # 计算相对于搜索根目录的相对路径
            rel_path = os.path.relpath(poster_dir, start=root_dir)
            # 构建输出目录路径
            output_dir = os.path.join(output_base_dir, rel_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 获取视频文件名（不含扩展名）
            video_filename = os.path.splitext(os.path.basename(video_file))[0]
            # strm文件名与视频同名，但扩展名为.strm
            strm_file_path = os.path.join(output_dir, f"{video_filename}.strm")
            
            # 写入视频文件路径到strm文件
            with open(strm_file_path, 'w', encoding='utf-8') as f:
                f.write(video_file)
            
            print(f"已创建strm文件: {strm_file_path} 指向视频文件: {video_file}")
            strm_file_paths.append((strm_file_path, width, height))  # 添加到列表中，包含分辨率信息
        else:
            print(f"警告: 在 {poster_dir} 中未找到大于300MB的视频文件")
    
    return strm_file_paths, output_base_dir  # 返回所有生成的strm文件路径和输出目录，包含分辨率信息

if __name__ == "__main__":
    # 初始化Tkinter但不显示主窗口
    root = tk.Tk()
    root.withdraw()
    
    # 打开路径选择器选择输入目录
    print("请选择要搜索的根目录...")
    root_dir = filedialog.askdirectory(title="选择要搜索的根目录")
    
    if not root_dir:
        print("未选择目录，程序退出")
        exit(1)
    
    # 查找小海报
    print("正在搜索分辨率高度小于540px的poster.jpg图片...")
    small_posters = find_small_posters(root_dir)
    
    if not small_posters:
        print("没有找到符合条件的poster.jpg图片")
    else:
        print(f"找到 {len(small_posters)} 个符合条件的poster.jpg图片")
        
        # 创建strm文件
        print(f"正在创建strm文件...")
        strm_file_paths, output_base_dir = create_strm_files(small_posters, root_dir)
        
        # 将所有strm文件路径和分辨率写入poster-min.txt，带编号
        output_list_file = os.path.join(output_base_dir, "poster-min.txt")
        with open(output_list_file, 'w', encoding='utf-8') as f:
            for i, (path, width, height) in enumerate(strm_file_paths, 1):  # 从1开始编号
                f.write(f"{i}. {path} (分辨率: {width}x{height})\n")
        
        print(f"操作完成，共生成 {len(strm_file_paths)} 个strm文件")
        print(f"所有strm文件路径和分辨率已保存到: {output_list_file}")
        print("输出文件包含编号列表，格式为: 编号. 路径 (分辨率: 宽x高)")
