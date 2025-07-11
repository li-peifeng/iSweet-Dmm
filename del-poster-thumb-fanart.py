import os
import tkinter as tk
from tkinter import filedialog

def find_and_delete_files(directory, filenames_to_delete):
    """
    递归查找并删除指定文件名的文件
    :param directory: 要搜索的目录
    :param filenames_to_delete: 要删除的文件名列表
    """
    deleted_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file in filenames_to_delete:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    deleted_files.append(file_path)
                    print(f"已删除: {file_path}")
                except Exception as e:
                    print(f"删除失败: {file_path} - 错误: {e}")
    
    return deleted_files

def main():
    # 创建Tkinter根窗口但不显示
    root = tk.Tk()
    root.withdraw()
    
    # 打开文件夹选择对话框
    print("请选择要搜索的目录...")
    directory = filedialog.askdirectory(title="选择要搜索的目录")
    
    if not directory:
        print("未选择目录，程序退出。")
        return
    
    # 要删除的文件名列表
    filenames_to_delete = ['poster.jpg', 'thumb.jpg', 'fanart.jpg']
    
    print(f"开始在目录 {directory} 中搜索并删除以下文件: {filenames_to_delete}")
    
    # 查找并删除文件
    deleted_files = find_and_delete_files(directory, filenames_to_delete)
    
    print("\n操作完成。")
    if deleted_files:
        print(f"共删除了 {len(deleted_files)} 个文件:")
        for file_path in deleted_files:
            print(f"  - {file_path}")
    else:
        print("没有找到匹配的文件。")

if __name__ == "__main__":
    main()