import os
import subprocess
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from datetime import datetime

def select_directory(title):
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title=title)
    return folder if folder else None

def process_images(input_dir, output_dir):
    # 初始化日志文件
    log_file = os.path.join(output_dir, "ai.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"图片处理日志 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"源目录: {input_dir}\n")
        f.write(f"目标目录: {output_dir}\n")
        f.write("="*50 + "\n")
    
    # Upscayl配置
    upscayl_path = "/Applications/Upscayl.app/Contents/Resources/bin/upscayl-bin"
    model_path = "/Applications/Upscayl.app/Contents/Resources/models"
    model_name = "remacri-4x"

    for root, dirs, files in os.walk(input_dir):
        # 忽略extrafanart文件夹
        if "extrafanart" in dirs:
            dirs.remove("extrafanart")
        
        # 获取相对于输入目录的相对路径
        relative_path = os.path.relpath(root, input_dir)
        output_subdir = os.path.join(output_dir, relative_path)
        
        # 创建对应的输出子目录
        os.makedirs(output_subdir, exist_ok=True)
        
        for file in files:
            file_path = os.path.join(root, file)
            file_lower = file.lower()
            
            # 只处理poster.jpg和thumb.jpg
            if file_lower not in ["poster.jpg", "thumb.jpg"]:
                continue
                
            if file_lower == "poster.jpg":
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                    
                    if height <= 540:
                        output_path = os.path.join(output_subdir, file)
                        
                        cmd = [
                            upscayl_path,
                            "-i", file_path,
                            "-o", output_path,
                            "-m", model_path,
                            "-n", model_name,
                            "-s", "4",
                            "-c", "95",
                            "-f", "jpg"
                        ]
                        
                        try:
                            result = subprocess.run(cmd, check=True, timeout=300,
                                                  stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                            
                            if os.path.exists(output_path):
                                log_msg = f"[PROCESSED] {datetime.now().strftime('%H:%M:%S')} | poster.jpg (原始高度:{height}px) | 源路径: {file_path} | 目标路径: {output_path}"
                                print(f"✓ {log_msg}")
                                with open(log_file, "a", encoding="utf-8") as f:
                                    f.write(log_msg + "\n")
                            else:
                                error_msg = f"[FAILED] {datetime.now().strftime('%H:%M:%S')} | 输出文件未生成 | 命令: {' '.join(cmd)}"
                                print(f"× {error_msg}")
                                with open(log_file, "a", encoding="utf-8") as f:
                                    f.write(error_msg + "\n")
                        
                        except subprocess.TimeoutExpired:
                            error_msg = f"[TIMEOUT] {datetime.now().strftime('%H:%M:%S')} | 处理超时: {file_path}"
                            print(f"× {error_msg}")
                            with open(log_file, "a", encoding="utf-8") as f:
                                f.write(error_msg + "\n")
                        
                        except subprocess.CalledProcessError as e:
                            error_msg = f"[ERROR] {datetime.now().strftime('%H:%M:%S')} | 处理失败(代码{e.returncode}): {file_path} | 错误: {e.stderr.decode().strip()}"
                            print(f"× {error_msg}")
                            with open(log_file, "a", encoding="utf-8") as f:
                                f.write(error_msg + "\n")
                    
                    else:
                        log_msg = f"[SKIPPED] {datetime.now().strftime('%H:%M:%S')} | poster.jpg (高度:{height}px > 540px) | 路径: {file_path}"
                        print(f"↻ {log_msg}")
                        with open(log_file, "a", encoding="utf-8") as f:
                            f.write(log_msg + "\n")
                
                except Exception as e:
                    error_msg = f"[ERROR] {datetime.now().strftime('%H:%M:%S')} | 读取失败: {file_path} | 错误: {str(e)}"
                    print(f"× {error_msg}")
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(error_msg + "\n")
            
            elif file_lower == "thumb.jpg":
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                    
                    if width <= 800:
                        output_path = os.path.join(output_subdir, "thumb.jpg")
                        fanart_path = os.path.join(output_subdir, "fanart.jpg")
                        new_width = int((1200 / height) * width)
                        
                        cmd = [
                            upscayl_path,
                            "-i", file_path,
                            "-o", output_path,
                            "-m", model_path,
                            "-n", model_name,
                            "-s", "4",
                            "-r", f"{new_width}x1200",
                            "-c", "95",
                            "-f", "jpg"
                        ]
                        
                        try:
                            result = subprocess.run(cmd, check=True, timeout=300,
                                                  stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                            
                            if os.path.exists(output_path):
                                # 复制为fanart.jpg
                                shutil.copy2(output_path, fanart_path)
                                
                                log_msg = f"[PROCESSED] {datetime.now().strftime('%H:%M:%S')} | thumb.jpg (原始尺寸: {width}x{height}px → 新尺寸: {new_width}x1200px) | 源路径: {file_path} | 目标路径: {output_path}"
                                print(f"✓ {log_msg}")
                                with open(log_file, "a", encoding="utf-8") as f:
                                    f.write(log_msg + "\n")
                                    f.write(f"      | 生成副本: {fanart_path}\n")
                            else:
                                error_msg = f"[FAILED] {datetime.now().strftime('%H:%M:%S')} | 输出文件未生成 | 命令: {' '.join(cmd)}"
                                print(f"× {error_msg}")
                                with open(log_file, "a", encoding="utf-8") as f:
                                    f.write(error_msg + "\n")
                        
                        except subprocess.TimeoutExpired:
                            error_msg = f"[TIMEOUT] {datetime.now().strftime('%H:%M:%S')} | 处理超时: {file_path}"
                            print(f"× {error_msg}")
                            with open(log_file, "a", encoding="utf-8") as f:
                                f.write(error_msg + "\n")
                        
                        except subprocess.CalledProcessError as e:
                            error_msg = f"[ERROR] {datetime.now().strftime('%H:%M:%S')} | 处理失败(代码{e.returncode}): {file_path} | 错误: {e.stderr.decode().strip()}"
                            print(f"× {error_msg}")
                            with open(log_file, "a", encoding="utf-8") as f:
                                f.write(error_msg + "\n")
                    
                    else:
                        log_msg = f"[SKIPPED] {datetime.now().strftime('%H:%M:%S')} | thumb.jpg (宽度:{width}px > 800px) | 路径: {file_path}"
                        print(f"↻ {log_msg}")
                        with open(log_file, "a", encoding="utf-8") as f:
                            f.write(log_msg + "\n")
                
                except Exception as e:
                    error_msg = f"[ERROR] {datetime.now().strftime('%H:%M:%S')} | 读取失败: {file_path} | 错误: {str(e)}"
                    print(f"× {error_msg}")
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(error_msg + "\n")

if __name__ == "__main__":
    print("=== 图片处理工具 ===")
    print("规则说明:")
    print("  - 只处理 poster.jpg 和 thumb.jpg")
    print("  - poster.jpg: 高度≤540px → 优化后复制到目标目录")
    print("  - poster.jpg: 高度>540px → 不做任何处理")
    print("  - thumb.jpg: 宽度≤800px → 优化并生成fanart.jpg到目标目录")
    print("  - thumb.jpg: 宽度>800px → 不做任何处理")
    print("  - 忽略所有其他文件和extrafanart文件夹")
    print("  - 将保留原始目录结构")
    print("  - 所有操作将记录到目标目录的ai.txt")
    print("  - 原始文件不会被修改或删除")
    
    input_dir = select_directory("选择源图片目录")
    
    if input_dir:
        output_dir = select_directory("选择目标目录")
        if output_dir:
            print(f"开始处理: 从 {input_dir} 到 {output_dir}")
            process_images(input_dir, output_dir)
            print(f"处理完成! 日志已保存到: {os.path.join(output_dir, 'ai.txt')}")
        else:
            print("未选择目标目录，已退出")
    else:
        print("未选择源目录，已退出")