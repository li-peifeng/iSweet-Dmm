import os
import sys
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def select_directory():
    """打开目录选择对话框"""
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="请选择要处理的目录")
    return directory if directory else None

def get_image_resolution(file_path):
    """获取图片分辨率"""
    try:
        with Image.open(file_path) as img:
            return img.size  # (width, height)
    except Exception as e:
        print(f"无法打开图片 {file_path}: {e}", file=sys.stderr)
        return None

def process_images_and_strm(directory, results):
    """处理图片文件和.strm文件"""
    for root, _, files in os.walk(directory, topdown=False):
        poster_path = None
        thumb_path = None
        strm_files = []
        
        # 分类文件
        for file in files:
            if file.lower() == 'poster.jpg':
                poster_path = os.path.join(root, file)
            elif file.lower() == 'thumb.jpg':
                thumb_path = os.path.join(root, file)
            elif file.lower().endswith('.strm'):
                strm_files.append(os.path.join(root, file))
        
        has_valid_images = False
        
        # 先处理thumb.jpg（如果存在）
        if thumb_path:
            resolution = get_image_resolution(thumb_path)
            if resolution:
                width, height = resolution
                max_side = max(width, height)
                if max_side <= 800:
                    # 删除长边≤800px的thumb.jpg
                    try:
                        os.remove(thumb_path)
                        results.append(f"删除: {thumb_path} (长边 {max_side}px ≤ 800px)")
                        thumb_path = None  # 标记为已删除
                    except Exception as e:
                        results.append(f"错误: 无法删除 {thumb_path}: {e}")
                else:
                    has_valid_images = True  # 有有效的thumb.jpg
        
        # 处理poster.jpg（如果存在）
        if poster_path:
            resolution = get_image_resolution(poster_path)
            if resolution:
                width, height = resolution
                if height < 540:
                    # 删除高度小于540px的poster.jpg
                    try:
                        os.remove(poster_path)
                        results.append(f"删除: {poster_path} (高度 {height}px < 540px)")
                    except Exception as e:
                        results.append(f"错误: 无法删除 {poster_path}: {e}")
                else:
                    # 处理高度≥540px的poster.jpg
                    if thumb_path:  # 这里thumb_path存在说明它通过了前面的检查（长边>800px）
                        # 将thumb.jpg重命名为hi-thumb.jpg
                        hi_thumb_path = os.path.join(root, 'hi-thumb.jpg')
                        try:
                            os.rename(thumb_path, hi_thumb_path)
                            results.append(f"重命名: {thumb_path} -> {hi_thumb_path}")
                        except Exception as e:
                            results.append(f"错误: 无法重命名 {thumb_path} -> {hi_thumb_path}: {e}")
                    
                    # 将poster.jpg重命名为thumb.jpg
                    new_thumb_path = os.path.join(root, 'thumb.jpg')
                    try:
                        os.rename(poster_path, new_thumb_path)
                        results.append(f"重命名: {poster_path} -> {new_thumb_path}")
                        has_valid_images = True
                    except Exception as e:
                        results.append(f"错误: 无法重命名 {poster_path} -> {new_thumb_path}: {e}")
        
        # 检查是否需要保留.strm文件
        if not has_valid_images and strm_files:
            # 如果没有有效的图片文件，删除所有.strm文件
            for strm_file in strm_files:
                try:
                    os.remove(strm_file)
                    results.append(f"删除: {strm_file} (无有效图片文件)")
                except Exception as e:
                    results.append(f"错误: 无法删除 {strm_file}: {e}")

def delete_empty_directories(directory, results):
    """递归删除空目录"""
    deleted = True
    while deleted:
        deleted = False
        for root, dirs, files in os.walk(directory, topdown=False):
            if not dirs and not files:
                try:
                    os.rmdir(root)
                    results.append(f"删除空目录: {root}")
                    deleted = True
                except OSError:
                    pass

def save_results(directory, results):
    """保存处理结果到文件"""
    output_file = os.path.join(directory, 'poster-thumb-rename.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(results))

def main():
    # 选择目录
    directory = select_directory()
    if not directory:
        print("未选择目录，程序退出", file=sys.stderr)
        sys.exit(0)
    
    print(f"开始处理目录: {directory}", file=sys.stderr)
    results = []
    
    # 处理图片和.strm文件
    process_images_and_strm(directory, results)
    
    # 删除空目录
    delete_empty_directories(directory, results)
    
    # 保存结果
    save_results(directory, results)
    
    print(f"处理完成，结果已保存到: {os.path.join(directory, 'poster-thumb-rename.txt')}", file=sys.stderr)
    
    # 输出摘要
    print("\n处理摘要:", file=sys.stderr)
    for result in results[:10]:  # 只显示前10条结果
        print(result, file=sys.stderr)
    if len(results) > 10:
        print(f"...(共 {len(results)} 条结果，完整结果已保存到文件)", file=sys.stderr)

if __name__ == "__main__":
    main()