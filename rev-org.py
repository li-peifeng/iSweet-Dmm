import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def compare_images(img1_path, img2_path):
    """比较两个图片的像素大小，返回像素较大的图片路径"""
    try:
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)
        
        pixels1 = img1.size[0] * img1.size[1]
        pixels2 = img2.size[0] * img2.size[1]
        
        return img1_path if pixels1 >= pixels2 else img2_path
    except Exception as e:
        print(f"比较图片时出错: {e}")
        return img1_path  # 如果出错，默认保留原文件

def rename_thumb_org_files(root_dir):
    """递归查找并重命名thumb-org.jpg文件"""
    count = 0
    conflicts = 0
    
    for root, _, files in os.walk(root_dir):
        thumb_org_path = os.path.join(root, 'thumb-org.jpg')
        
        if 'thumb-org.jpg' in files:
            thumb_path = os.path.join(root, 'thumb.jpg')
            poster_path = os.path.join(root, 'poster.jpg')
            
            if os.path.exists(thumb_path):
                # 如果thumb.jpg存在，先检查poster.jpg是否存在
                if os.path.exists(poster_path):
                    # 比较两个poster.jpg的像素
                    better_poster = compare_images(thumb_path, poster_path)
                    
                    if better_poster == thumb_path:
                        # 如果thumb.jpg更好，替换poster.jpg
                        os.replace(poster_path, poster_path + '.bak')  # 先备份
                        os.replace(thumb_path, poster_path)
                        print(f"已替换较差的poster.jpg在: {root}")
                        conflicts += 1
                    else:
                        # 如果原poster.jpg更好，直接删除thumb.jpg
                        os.remove(thumb_path)
                        print(f"保留原poster.jpg在: {root}")
                        conflicts += 1
                else:
                    # 如果poster.jpg不存在，将thumb.jpg重命名为poster.jpg
                    os.rename(thumb_path, poster_path)
                    print(f"已将thumb.jpg重命名为poster.jpg在: {root}")
                    conflicts += 1
            
            # 最后将thumb-org.jpg重命名为thumb.jpg
            os.rename(thumb_org_path, thumb_path)
            print(f"已将thumb-org.jpg重命名为thumb.jpg在: {root}")
            count += 1
    
    print(f"\n操作完成！")
    print(f"共重命名了 {count} 个thumb-org.jpg文件")
    print(f"共处理了 {conflicts} 个冲突情况")

def select_directory():
    """选择目录的GUI"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    folder_selected = filedialog.askdirectory(title="请选择包含thumb-org.jpg的目录")
    
    if folder_selected:
        print(f"已选择目录: {folder_selected}")
        rename_thumb_org_files(folder_selected)
    else:
        print("未选择目录，程序退出。")

if __name__ == "__main__":
    select_directory()