import os
import shutil
import json
import frontmatter

# --- V11.0 (Manual Command Edition) ---
# 移除了所有自动搜索功能，当配置失效时，将直接请求用户手动输入。

# --- 1. 全局配置 ---
# 你的Obsidian发布库的绝对路径 D:\\兴趣爱好\\LingMing's Library\\LingMing的core小世界
CONFIG_FILE_NAME = "deploy_config.json"
project_root = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(project_root, CONFIG_FILE_NAME)
target_dir = os.path.join(project_root, "content")

# --- 2. 核心功能模块 (已简化) ---

def load_config():
    """尝试加载配置，如果配置文件存在且其中路径有效，则返回配置"""
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                config = json.load(f)
                source_dir = config.get("source_dir")
                # 核心检查：路径不仅要存在，还必须是一个文件夹
                if source_dir and os.path.isdir(source_dir):
                    return config
            except (json.JSONDecodeError, TypeError):
                # 如果文件内容为空或格式错误，则认为配置无效
                return None
    return None

def save_config(source_dir):
    """将新的配置保存到文件"""
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump({"source_dir": source_dir}, f, indent=4)
    print(f"\n配置已保存，已将您的Obsidian库绑定到: {source_dir}")

def prompt_for_manual_path():
    """【手动指令模式】直接请求用户在命令行中输入路径"""
    print("\n未能找到有效的配置文件，需要您手动绑定Obsidian库。")
    while True:
        manual_path = input("请输入您的Obsidian库的完整文件夹路径: ").strip()
        # 验证路径是否是一个有效的Obsidian库（判断是否存在.obsidian子文件夹）
        if os.path.isdir(manual_path) and os.path.isdir(os.path.join(manual_path, '.obsidian')):
            save_config(manual_path)
            return {"source_dir": manual_path}
        else:
            print("错误：路径无效，或该路径下未找到'.obsidian'文件夹。请确保输入的是Obsidian库的根目录。")

# --- 3. 主同步逻辑 (保持v8.0的确定性内核) ---
def sync_notes(source_dir):
    print("\n--- 确定性同步引擎启动 ---")
    
    # 【清扫铁律】
    print("步骤1/3: 正在清扫旧文件...")
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    post = frontmatter.load(file_path, encoding='utf-8')
                    if post.get('publish') is True:
                        os.remove(file_path)
                except Exception:
                    continue
    
    # 【部署铁律】
    print("步骤2/3: 正在部署新文件...")
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".md"):
                source_file_path = os.path.join(root, file)
                try:
                    post = frontmatter.load(source_file_path, encoding='utf-8')
                    if post.get('publish') is True:
                        relative_path = os.path.relpath(root, source_dir)
                        destination_dir = os.path.join(target_dir, relative_path)
                        if not os.path.exists(destination_dir):
                            os.makedirs(destination_dir)
                        shutil.copy2(source_file_path, destination_dir)
                except Exception:
                    continue
                    
    # 【清理空巢】
    print("步骤3/3: 正在清理空文件夹...")
    for root, dirs, _ in os.walk(target_dir, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            if os.path.exists(dir_path) and not os.listdir(dir_path):
                os.rmdir(dir_path)

# --- 4. 程序主入口 ---
def main():
    print("--- V11.0 '手动指令'同步系统启动 ---")
    config = load_config()
    
    if not config:
        config = prompt_for_manual_path()

    if config:
        source_dir = config["source_dir"]
        print(f"\n当前绑定的Obsidian库: {source_dir}")
        sync_notes(source_dir)
        print("\n--- V11.0 同步任务圆满完成 ---")
    else:
        # 理论上在循环中不会到达这里，作为最终保险
        print("\n--- 任务中止：未能获取有效的Obsidian库路径。 ---")

if __name__ == "__main__":
    main()