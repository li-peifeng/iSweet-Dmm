# 此脚本复制刮削好的poster和thumb到视频文件夹，注意必须保持目录结构完全一样！

import os
import shutil
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

def get_directory(title):
    """使用GUI选择目录"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    directory = filedialog.askdirectory(title=title)
    return directory

def get_image_dimensions(image_path):
    """获取图片的尺寸"""
    with Image.open(image_path) as img:
        return img.size  # 返回 (width, height)

def move_with_structure(src_dir, dst_dir, file_path, file_type):
    """
    移动文件到目标目录，保持相同的目录结构
    如果目标文件已存在，比较分辨率，保留分辨率高的文件
    移动后删除源文件和所在文件夹中的所有strm文件，以及可能的空文件夹
    """
    # 获取相对于源目录的相对路径
    rel_path = os.path.relpath(file_path, src_dir)
    # 构建目标路径
    dst_path = os.path.join(dst_dir, rel_path)
    
    print(f"处理{file_type}文件: {file_path}")
    print(f"相对路径: {rel_path}")
    print(f"目标路径: {dst_path}")
    
    # 确保目标目录存在
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    
    # 检查目标文件是否已存在
    if os.path.exists(dst_path):
        # 获取源文件和目标文件的尺寸
        src_width, src_height = get_image_dimensions(file_path)
        dst_width, dst_height = get_image_dimensions(dst_path)
        
        print(f"目标{file_type}文件已存在: {dst_path}")
        print(f"源{file_type}文件分辨率: {src_width}x{src_height}, 目标{file_type}文件分辨率: {dst_width}x{dst_height}")
        
        if (src_width, src_height) > (dst_width, dst_height):
            # 源文件分辨率更高，覆盖目标文件(先删除目标文件)
            print(f"源{file_type}文件分辨率更高，覆盖目标{file_type}文件")
            os.remove(dst_path)
            shutil.move(file_path, dst_path)
            print(f"覆盖并移动{file_type}文件: {dst_path} (源分辨率: {src_width}x{src_height}, 目标分辨率: {dst_width}x{dst_height})")
        else:
            # 目标文件分辨率更高或相等，删除源文件
            print(f"目标{file_type}文件分辨率更高或相等，删除源{file_type}文件")
            os.remove(file_path)
            print(f"跳过移动{file_type}文件: {file_path} (源分辨率: {src_width}x{src_height}, 目标分辨率: {dst_width}x{dst_height})")
            
            # 删除源文件所在目录中的所有strm文件
            src_folder = os.path.dirname(file_path)
            delete_strm_files_in_folder(src_folder)
            
            # 检查并删除空文件夹
            check_and_delete_empty_folders(src_folder, src_dir)
            
            return  # 不需要继续处理，因为源文件已被删除
    else:
        # 目标文件不存在，直接移动
        print(f"目标{file_type}文件不存在，直接移动")
        shutil.move(file_path, dst_path)
        print(f"移动{file_type}文件: {dst_path}")
    
    # 删除源文件所在目录中的所有strm文件
    src_folder = os.path.dirname(file_path)
    delete_strm_files_in_folder(src_folder)
    
    # 检查并删除空文件夹
    check_and_delete_empty_folders(src_folder, src_dir)

def delete_strm_files_in_folder(folder_path):
    """
    删除指定文件夹中的所有.strm文件
    """
    try:
        print(f"开始检查文件夹中的strm文件: {folder_path}")
        # 获取文件夹中的所有文件
        files = os.listdir(folder_path)
        # 筛选出所有.strm文件
        strm_files = [f for f in files if f.lower().endswith('.strm')]
        
        if not strm_files:
            print(f"文件夹中没有strm文件: {folder_path}")
            return
        
        # 删除所有strm文件
        for strm_file in strm_files:
            strm_file_path = os.path.join(folder_path, strm_file)
            print(f"删除strm文件: {strm_file_path}")
            os.remove(strm_file_path)
        
        print(f"共删除了 {len(strm_files)} 个strm文件")
    except Exception as e:
        print(f"删除strm文件时出错: {folder_path}, 错误: {str(e)}")

def check_and_delete_empty_folders(folder_path, src_dir):
    """
    从指定文件夹开始向上检查并删除空文件夹
    只有当文件夹中既没有poster.jpg也没有.thumb.jpg文件时才删除
    """
    try:
        print(f"开始检查空文件夹: {folder_path}")
        current_dir = folder_path
        
        # 我们需要持续检查父文件夹，直到到达源目录
        while current_dir != src_dir:  # 不要删除源目录本身
            # 检查当前文件夹是否为空（没有poster.jpg和.thumb.jpg文件）
            if is_folder_empty(current_dir, src_dir):
                print(f"文件夹符合条件，准备删除: {current_dir}")
                os.rmdir(current_dir)
                print(f"删除空文件夹: {current_dir}")
                # 移动到上一级目录继续检查
                current_dir = os.path.dirname(current_dir)
            else:
                print(f"文件夹不符合删除条件: {current_dir}")
                break  # 文件夹不为空，停止向上检查
        
        print("完成检查空文件夹")
    except Exception as e:
        # 删除文件夹时出错（可能由于权限或其他原因），忽略错误继续执行
        print(f"检查并删除空文件夹时出错: {folder_path}, 错误: {str(e)}")

def is_folder_empty(folder_path, src_dir):
    """
    检查文件夹是否为空（没有poster.jpg和.thumb.jpg文件）
    注意：这个函数只检查直接子文件，不递归检查子文件夹
    """
    try:
        # 获取文件夹中的所有文件
        files = os.listdir(folder_path)
        
        # 检查是否有poster.jpg或.thumb.jpg文件
        has_poster_jpg = "poster.jpg" in files
        has_thumb_jpg = "thumb.jpg" in files
        has_strm_files = any(f.lower().endswith('.strm') for f in files)
        
        # 如果既没有poster.jpg也没有.thumb.jpg和.strm文件，则认为文件夹为空
        return not (has_poster_jpg or has_thumb_jpg or has_strm_files)
    except Exception as e:
        print(f"检查文件夹是否为空时出错: {folder_path}, 错误: {str(e)}")
        return False  # 如果出现错误，保守地认为文件夹不为空

def find_and_move_posters_and_thumbs(src_dir, dst_dir):
    """查找并移动符合条件的poster.jpg和thumb.jpg文件"""
    # 查找所有符合条件的poster.jpg文件
    poster_files = []
    thumb_files = []
    
    for root, dirs, files in os.walk(src_dir):
        if "poster.jpg" in files:
            file_path = os.path.join(root, "poster.jpg")
            width, height = get_image_dimensions(file_path)
            if height > 538:
                poster_files.append(file_path)
                print(f"找到符合条件的poster文件: {file_path} (分辨率: {width}x{height})")
        
        if "thumb.jpg" in files:
            file_path = os.path.join(root, "thumb.jpg")
            width, height = get_image_dimensions(file_path)
            # 对于thumb.jpg，我们不做高度限制，只要存在就处理
            thumb_files.append(file_path)
            print(f"找到thumb文件: {file_path} (分辨率: {width}x{height})")
    
    if not poster_files and not thumb_files:
        messagebox.showinfo("结果", "没有找到符合条件的poster.jpg或thumb.jpg文件")
        return
    
    print(f"共找到 {len(poster_files)} 个符合条件的poster文件和 {len(thumb_files)} 个thumb文件")
    
    # 让用户选择输出目录
    dst_dir = get_directory("选择输出目录")
    if not dst_dir:
        messagebox.showinfo("取消", "用户取消了输出目录选择")
        return
    
    # 移动文件，严格验证目录结构
    error_occurred = False
    for file_path in poster_files:
        try:
            # 获取相对于源目录的相对路径
            rel_path = os.path.relpath(file_path, src_dir)
            # 构建目标路径
            dst_path = os.path.join(dst_dir, rel_path)
            
            # 检查目标路径的父目录是否存在
            dst_parent = os.path.dirname(dst_path)
            if not os.path.exists(dst_parent):
                messagebox.showerror("错误", f"目标目录结构不一致。缺少目录: {dst_parent}")
                error_occurred = True
                break
            
            # 移动文件
            print(f"\n开始处理poster文件: {file_path}")
            move_with_structure(src_dir, dst_dir, file_path, "poster")
            print(f"完成处理poster文件: {file_path}\n")
        except Exception as e:
            messagebox.showerror("错误", f"移动poster文件 {file_path} 时出错: {str(e)}")
            error_occurred = True
            break
    
    for file_path in thumb_files:
        try:
            # 获取相对于源目录的相对路径
            rel_path = os.path.relpath(file_path, src_dir)
            # 构建目标路径
            dst_path = os.path.join(dst_dir, rel_path)
            
            # 检查目标路径的父目录是否存在
            dst_parent = os.path.dirname(dst_path)
            if not os.path.exists(dst_parent):
                messagebox.showerror("错误", f"目标目录结构不一致。缺少目录: {dst_parent}")
                error_occurred = True
                break
            
            # 移动文件
            print(f"\n开始处理thumb文件: {file_path}")
            move_with_structure(src_dir, dst_dir, file_path, "thumb")
            print(f"完成处理thumb文件: {file_path}\n")
        except Exception as e:
            messagebox.showerror("错误", f"移动thumb文件 {file_path} 时出错: {str(e)}")
            error_occurred = True
            break
    
    if not error_occurred:
        messagebox.showinfo("完成", f"成功移动了 {len(poster_files)} 个poster文件和 {len(thumb_files)} 个thumb文件")

def main():
    # 选择输入目录
    src_dir = get_directory("选择输入目录")
    if not src_dir:
        messagebox.showinfo("取消", "用户取消了输入目录选择")
        return
    
    print(f"选择的源目录: {src_dir}")
    
    # 查找并移动文件
    find_and_move_posters_and_thumbs(src_dir, None)  # dst_dir会在函数中让用户选择

if __name__ == "__main__":
    main()