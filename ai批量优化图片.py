import os
import subprocess
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from datetime import datetime

def select_directory():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="选择图片目录")
    return folder if folder else None

def process_images(input_dir):
    # 初始化日志文件
    log_file = os.path.join(input_dir, "ai.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"图片处理日志 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*50 + "\n")
    
    # Upscayl配置
    upscayl_path = "/Applications/Upscayl.app/Contents/Resources/bin/upscayl-bin"
    model_path = "/Applications/Upscayl.app/Contents/Resources/models"
    model_name = "remacri-4x"

    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            if file.lower() == "poster.jpg":
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                    
                    if height <= 538:
                        os.remove(file_path)
                        log_msg = f"[DELETED] {datetime.now().strftime('%H:%M:%S')} | poster.jpg (高度:{height}px) | 路径: {file_path}"
                        print(f"🗑️ {log_msg}")
                        with open(log_file, "a", encoding="utf-8") as f:
                            f.write(log_msg + "\n")
                    else:
                        log_msg = f"[SKIPPED] {datetime.now().strftime('%H:%M:%S')} | poster.jpg (高度:{height}px > 538px) | 路径: {file_path}"
                        print(f"↻ {log_msg}")
                        with open(log_file, "a", encoding="utf-8") as f:
                            f.write(log_msg + "\n")
                
                except Exception as e:
                    error_msg = f"[ERROR] {datetime.now().strftime('%H:%M:%S')} | 读取失败: {file_path} | 错误: {str(e)}"
                    print(f"× {error_msg}")
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(error_msg + "\n")
            
            elif file.lower() == "thumb.jpg":
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                    
                    if width <= 800:
                        output_path = os.path.join(root, "thumb_upscaled.jpg")
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
                                # 覆盖原文件
                                os.replace(output_path, file_path)
                                
                                # 复制为fanart.jpg
                                fanart_path = os.path.join(root, "fanart.jpg")
                                shutil.copy2(file_path, fanart_path)
                                
                                log_msg = f"[PROCESSED] {datetime.now().strftime('%H:%M:%S')} | thumb.jpg (原始尺寸: {width}x{height}px → 新尺寸: {new_width}x1200px) | 路径: {file_path}"
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
    print("  - poster.jpg: 高度≤538px → 直接删除")
    print("  - thumb.jpg: 宽度≤800px → 优化并生成fanart.jpg")
    print("  - 所有操作将记录到 ai.txt")
    
    input_dir = select_directory()
    
    if input_dir:
        print(f"开始处理目录: {input_dir}")
        process_images(input_dir)
        print(f"处理完成! 日志已保存到: {os.path.join(input_dir, 'ai.txt')}")
    else:
        print("未选择目录，已退出")