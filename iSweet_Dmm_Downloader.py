# iSweet_Dmm_图片下载器 By PeiFeng.Li
import os
import re
import sys
import requests
import tkinter as tk
from tkinter import filedialog
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# 配置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/119.0.0.0 Safari/537.36'
}

def format_code(raw_code):
    """格式化产品代码，处理所有后缀和格式"""
    # 清理数字后的后缀（包括-UMR/-U/-L/-C等）
    cleaned_code = re.sub(r'(?<=\d)-[A-Za-z-]+$', '', raw_code)
    
    # 分离字母和数字部分
    match = re.match(r'^([a-zA-Z]+)[-]?(\d+)$', cleaned_code)
    if not match:
        return None
    
    letters = match.group(1).lower()
    numbers = match.group(2)
    
    # 验证数字长度并补零
    if len(numbers) > 5:
        return None
    formatted_num = f"{int(numbers):05d}"
    
    return f"{letters}-{formatted_num}"

def download_files(formatted_code, save_path, download_type):
    """根据下载类型下载并保存文件（内存优先方案）"""
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1)
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    os.makedirs(save_path, exist_ok=True)
    tasks = []
    error_messages = []
    downloaded_files = set()

    # 配置下载任务
    if download_type == 'poster':
        tasks.append(('ps', ['poster.jpg']))
    elif download_type == 'thumb':
        tasks.append(('pl', ['thumb.jpg']))
    elif download_type == 'dual':
        tasks.append(('pl', ['fanart.jpg', 'thumb.jpg']))
    elif download_type == 'all':
        tasks.append(('ps', ['poster.jpg']))
        tasks.append(('pl', ['fanart.jpg', 'thumb.jpg']))

    for url_suffix, file_names in tasks:
        content = None
        try:
            # 获取下载内容到内存
            dmm_code = formatted_code.replace('-', '')
            url = f"https://awsimgsrc.dmm.co.jp/pics_dig/digital/video/{dmm_code}/{dmm_code}{url_suffix}.jpg"
            response = session.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # 内存校验
            content = response.content
            if len(content) < 30720:
                raise ValueError(f"文件小于30KB，已丢弃: {url}")

            # 写入文件
            for file_name in file_names:
                file_path = os.path.join(save_path, file_name)
                with open(file_path, 'wb') as f:
                    f.write(content)
                downloaded_files.add(file_name)

        except requests.exceptions.HTTPError:
            error_messages.append(f" ❌ 未找到此番号的封面图")
        except Exception as e:
            error_messages.append(f" ❌ 下载失败: {str(e)}")

    # 清理空目录（仅当完全没有下载成功时）
    if not downloaded_files:
        if os.path.exists(save_path) and not os.listdir(save_path):
            os.rmdir(save_path)
        return False, error_messages
    return True, error_messages

def get_leaf_folders(path):
    """获取所有叶子文件夹路径"""
    folders = []
    for root, dirs, _ in os.walk(path):
        if not dirs:
            folders.append({
                "raw_name": os.path.basename(root),
                "full_path": root
            })
    return folders

def show_main_menu():
    """显示主菜单"""
    print("\n\n\n" + " iSweet_Dmm_图片下载器模式选择 ".center(50, '='))
    print("\n\n1. 自动模式（从末级文件夹名自动批量获取番号）")
    print("2. 手动模式（手动输入番号，多个用逗号分隔）")
    print("3. 退出程序")
    return input("\n\n请输入数字进行选择 (1-3): ").strip()

def show_download_menu():
    """显示下载类型菜单（已按新要求调整）"""
    print("\n\n\n" + " iSweet_Dmm_图片下载器主菜单 ".center(50, '='))
    print("\n\n1. 竖版海报图 (Poster)")
    print("2. 横版缩略图 (Thumb)")
    print("3. 横版缩略图+背景图 (Thumb+Fanart)")
    print("4. 全部3种封面图 (Thumb+Poster+Fanart)")
    print("5. 返回主菜单")
    print("6. 退出程序")
    print("\n注：1/3/4选项适合不加水印，2适合加水印")
    return input("\n\n请输入数字进行选择 (1-6): ").strip()

def process_auto_mode(download_type):
    """处理自动模式"""
    root = tk.Tk()
    root.withdraw()
    source_dir = filedialog.askdirectory(title="选择根目录（取消返回主菜单）")
    if not source_dir:
        return 'back'
    
    print(f"\n ⏳ 正在扫描目录: {os.path.abspath(source_dir)}")
    folders = get_leaf_folders(source_dir)
    total = len(folders)
    success_count = 0
    partial_count = 0
    fail_count = 0

    for idx, folder in enumerate(folders, 1):
        raw_name = folder["raw_name"]
        folder_path = folder["full_path"]
        print(f"\n 🔍 正在处理: [{idx}/{total}] {raw_name}")
        
        formatted_code = format_code(raw_name)
        if not formatted_code:
            print(f" ❌ 番号格式无效: {raw_name}")
            fail_count += 1
            continue
        
        result, errors = download_files(formatted_code, folder_path, download_type)
        if result:
            success_count += 1
            msg = f" ✅ 下载成功！封面图已保存到: {folder_path}"
            if errors:
                partial_count += 1
                msg += f" ⚠️ 部分失败:未找到此番号的某些封面图"
            print(msg)
        else:
            print(f" ❌ 下载失败: 未找到此番号的封面图")
            fail_count += 1

    print(f"\n\n ✅ 自动模式完成")
    print(f" 🟩 成功下载: {success_count}")
    print(f" 🟧 部分失败: {partial_count}")
    print(f" 🟥 完全失败: {fail_count}")
    print(f" 🟦 合计处理: {total}")
    input("\n\n ↩️  返回主菜单...")
    return 'success'

def process_manual_mode(download_type):
    """处理手动模式"""
    while True:
        codes_input = input(" 🆎 请输入番号代码（多个用逗号分隔，输入back返回）: ").strip()
        if codes_input.lower() in ('back', 'exit', 'quit'):
            return 'back'
        
        codes = [c.strip() for c in codes_input.split(',') if c.strip()]
        if not codes:
            print(" ❌ 未输入有效的番号")
            continue
            
        total = len(codes)
        success_count = 0
        partial_count = 0
        fail_count = 0
        
        for idx, code in enumerate(codes, 1):
            print(f"\n 🔍 正在处理: [{idx}/{total}] {code}")
            
            formatted_code = format_code(code)
            if not formatted_code:
                print(f" ❌ 番号格式无效: {code}")
                fail_count += 1
                continue
            
            save_dir = os.path.join(os.getcwd(), "Thumb-Poster-Fanart", code)
            result, errors = download_files(formatted_code, save_dir, download_type)
            if result:
                success_count += 1
                msg = f" ✅ 成功！封面图已下载保存到: {save_dir}"
                if errors:
                    partial_count += 1
                    msg += f" ⚠️ 部分失败: {', '.join(errors)}"
                print(msg)
            else:
                print(f" ❌ 失败！下载失败: {', '.join(errors)}")
                fail_count += 1

        print(f"\n\n ✅ 手动模式成功完成 {success_count}/{total}")
        print(f" 🟩 成功下载: {success_count}")
        print(f" 🟧 部分失败: {partial_count}")
        print(f" 🟥 完全失败: {fail_count}")
        print(f" 🟦 合计处理: {total}")
        input("\n\n ↩️  返回主菜单...")
        return 'success'

def main():
    # 系统适配
    if sys.platform == 'darwin':
        os.environ['TK_SILENCE_DEPRECATION'] = '1'
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    current_download_type = 'dual'  # 默认下载类型
    
    while True:
        main_choice = show_main_menu()
        
        # 退出程序
        if main_choice == '3':
            confirm = input("\n\n ❓ 确认退出程序吗？(y/n): ").lower()
            if confirm == 'y':
                print("\n\n 🌐 PeiFeng.Li 祝你使用愉快，拜拜！💝 \n\n")
                sys.exit(0)
            continue
            
        # 初始化下载类型控制标记
        download_selected = False

        # 下载类型选择
        while True:
            dl_choice = show_download_menu()
            
            if dl_choice == '5':
                break  # 返回主菜单
            elif dl_choice == '6':
                confirm = input("\n\n ❓ 确认退出程序吗？(y/n): ").lower()
                if confirm == 'y':
                    print("\n\n 🌐 PeiFeng.Li 祝你使用愉快，拜拜！💝 \n\n")
                    sys.exit(0)
                continue
            elif dl_choice in ('1', '2', '3', '4'):
                current_download_type = {
                    '1': 'poster',
                    '2': 'thumb',
                    '3': 'dual',
                    '4': 'all'
                }[dl_choice]
                download_selected = True
                break
            else:
                print("❌ 无效输入，请重新选择")
                continue
        
        # 如果用户选择返回则跳过后续处理
        if not download_selected:
            continue
        
        # 处理模式选择
        if main_choice == '1':
            process_auto_mode(current_download_type)
        elif main_choice == '2':
            process_manual_mode(current_download_type)
        else:
            print("❌ 无效输入，请重新选择")

if __name__ == "__main__":
    main()