import os
import shutil
import json
from datetime import datetime
import frontmatter

# python deploy.py 启动命令
# --- V15.0 (Final & Elegant Edition) ---
# 采纳了“无publish即豁免”的核心逻辑，并修复所有已知Bug。

# --- 1. 全局配置 ---
CONFIG_FILE_NAME = "deploy_config.json"
project_root = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(project_root, CONFIG_FILE_NAME)
target_dir = os.path.join(project_root, "content")

# --- 2. 核心功能模块 ---
def load_config():
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                config = json.load(f)
                source_dir = config.get("source_dir")
                if source_dir and os.path.isdir(source_dir):
                    return config
            except (json.JSONDecodeError, TypeError):
                return None
    return None

def save_config(source_dir):
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump({"source_dir": source_dir}, f, indent=4)
    print(f"\n配置已保存，已将您的Obsidian库绑定到: {source_dir}")

def prompt_for_manual_path():
    print("\n未能找到有效的配置文件，需要您手动绑定Obsidian库。")
    while True:
        manual_path = input("请输入您的Obsidian库的完整文件夹路径: ").strip()
        if os.path.isdir(manual_path) and os.path.isdir(os.path.join(manual_path, '.obsidian')):
            save_config(manual_path)
            return {"source_dir": manual_path}
        else:
            print("错误：路径无效，或该路径下未找到'.obsidian'文件夹。请确保输入的是Obsidian库的根目录。")

# --- 3. V15.0 终极版核心同步逻辑 ---
def sync_notes(source_dir):
    print("\n--- 终极同步引擎 V15.0 '无Publish即豁免'启动 ---")
    
    # 【清扫铁律】(升级：逻辑与部署统一)
    print("\n步骤1/4: 正在清扫目标目录中需要更新的旧文件...")
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    post = frontmatter.load(file_path, encoding='utf-8')
                    # 只有明确标记为 publish: true 的文件才会被删除
                    if post.get('publish') is True:
                        os.remove(file_path)
                        print(f"  [清扫] 已删除旧版本文件: {file}")
                except Exception as e:
                    print(f"  [警告] 清扫时读取文件失败: {file}, 错误: {e}")
                    continue
    
    # 【部署、制证与反哺】(修复 NameError 并简化)
    print("\n步骤2/4: 正在处理并同步文件...")
    processed_files_count = 0  # ❗️修复：在这里初始化计数器
    for root, _, files in os.walk(source_dir):
        if '.obsidian' in root: continue
            
        for file in files:
            if file.endswith(".md"):
                source_file_path = os.path.join(root, file)
                try:
                    post = frontmatter.load(source_file_path, encoding='utf-8')
                    
                    # 核心逻辑：只处理明确需要发布的笔记
                    if post.get('publish') is True:
                        
                        needs_update = False
                        if 'title' not in post or not post['title']:
                            post['title'] = os.path.splitext(file)[0]
                            needs_update = True
                        if 'date' not in post:
                            post['date'] = datetime.fromtimestamp(os.path.getmtime(source_file_path)).isoformat()
                            needs_update = True
                        if post.get('draft') is not False:
                            post['draft'] = False
                            needs_update = True
                        
                        if needs_update:
                            updated_content_str = frontmatter.dumps(post)
                            with open(source_file_path, 'w', encoding='utf-8') as f:
                                f.write(updated_content_str)
                            print(f"  [反哺] 已更新源文件: {file}")

                        relative_path = os.path.relpath(root, source_dir)
                        destination_dir = os.path.join(target_dir, relative_path)
                        if not os.path.exists(destination_dir):
                            os.makedirs(destination_dir)
                        shutil.copy2(source_file_path, destination_dir)
                        processed_files_count += 1

                except Exception as e:
                    print(f"  [错误] 处理文件时出错: {source_file_path}, 信息: {e}")
                    continue
    
    print(f"  处理完成，共同步了 {processed_files_count} 个文件。")
                    
    # 【清理空巢】
    print("\n步骤3/4: 正在清理空文件夹...")
    for root, dirs, _ in os.walk(target_dir, topdown=False):
        # 避免删除 content 根目录
        if root == target_dir: continue
        for d in dirs:
            dir_path = os.path.join(root, d)
            if os.path.exists(dir_path) and not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"  [清理] 已删除空文件夹: {dir_path}")
            
    # 【创建中间页】
    print("\n步骤4/4: 正在检查并创建中间分类页...")
    for root, dirs, files in os.walk(target_dir):
        # 如果一个目录既没有 _index.md，也没有 index.md，我们就为它创建一个
        if '_index.md' not in files and 'index.md' not in files:
             # 但要排除根目录和空目录
            if root != target_dir and (dirs or files):
                dir_name = os.path.basename(root)
                index_file_path = os.path.join(root, '_index.md')
                with open(index_file_path, 'w', encoding='utf-8') as f:
                    f.write('---\n')
                    f.write(f'title: "{dir_name}"\n')
                    f.write('---\n')
                print(f"  [创建] 已为文件夹 '{dir_name}' 创建了索引页。")

# --- 4. 程序主入口 ---
def main():
    print("--- 终极同步引擎 V15.0 '无Publish即豁免'启动 ---")
    config = load_config()
    
    if not config:
        config = prompt_for_manual_path()

    if config:
        source_dir = config["source_dir"]
        print(f"\n当前绑定的Obsidian库: {source_dir}")
        sync_notes(source_dir)
        print("\n--- V15.0 同步任务圆满完成 ---")
    else:
        print("\n--- 任务中止：未能获取有效的Obsidian库路径。 ---")

if __name__ == "__main__":
    main()