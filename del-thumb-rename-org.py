import os
import tkinter as tk
from tkinter import filedialog

def select_directory():
    """打开目录选择对话框"""
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="请选择要处理的目录")
    return directory if directory else None

def process_files(directory):
    """递归处理文件"""
    results = []
    
    for root, _, files in os.walk(directory):
        # 查找并处理文件
        thumb_path = None
        hi_thumb_path = None
        strm_files = []
        
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower() == 'thumb.jpg':
                thumb_path = file_path
            elif file.lower() == 'hi-thumb.jpg':
                hi_thumb_path = file_path
            elif file.lower().endswith('.strm'):
                strm_files.append(file_path)
        
        # 删除thumb.jpg
        if thumb_path:
            try:
                os.remove(thumb_path)
                results.append(f"删除: {thumb_path}")
            except Exception as e:
                results.append(f"错误: 无法删除 {thumb_path}: {e}")
        
        # 删除.strm文件
        for strm_file in strm_files:
            try:
                os.remove(strm_file)
                results.append(f"删除: {strm_file}")
            except Exception as e:
                results.append(f"错误: 无法删除 {strm_file}: {e}")
        
        # 重命名hi-thumb.jpg为thumb.jpg
        if hi_thumb_path:
            new_thumb_path = os.path.join(root, 'thumb.jpg')
            try:
                os.rename(hi_thumb_path, new_thumb_path)
                results.append(f"重命名: {hi_thumb_path} -> {new_thumb_path}")
            except Exception as e:
                results.append(f"错误: 无法重命名 {hi_thumb_path}: {e}")
    
    return results

def save_results(directory, results):
    """保存处理结果到文件"""
    output_file = os.path.join(directory, 'file_operations_log.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(results))

def main():
    # 选择目录
    directory = select_directory()
    if not directory:
        print("未选择目录，程序退出")
        return
    
    print(f"开始处理目录: {directory}")
    results = process_files(directory)
    
    # 保存结果
    save_results(directory, results)
    
    print(f"处理完成，结果已保存到: {os.path.join(directory, 'file_operations_log.txt')}")
    
    # 输出摘要
    print("\n处理摘要:")
    for result in results[:10]:  # 只显示前10条结果
        print(result)
    if len(results) > 10:
        print(f"...(共 {len(results)} 条结果，完整结果已保存到文件)")

if __name__ == "__main__":
    main()