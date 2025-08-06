import os
import shutil
import frontmatter
import yaml

# --- 配置区 ---
# 你的Obsidian发布库的绝对路径
source_dir = "D:\\兴趣爱好\\LingMing's Library\\LingMing的core小世界" 
# Hugo的content文件夹的绝对路径
target_dir = "C:\\Users\\ROG\\my-blog-test-2\\content"
# --- 配置区结束 ---

def sync_notes():
    """
    同步Obsidian笔记到Hugo的content目录。
    1. 清空目标目录。
    2. 遍历源目录，寻找所有.md文件。
    3. 读取每个文件的frontmatter。
    4. 如果 frontmatter 中存在 `publish: true`，则将其复制到目标目录，并保持其原始的文件夹结构。
    """
    print("--- 开始同步任务 ---")

    # 1. 清空目标目录
    if os.path.exists(target_dir):
        print(f"正在清空目标文件夹: {target_dir}")
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)
    print("目标文件夹已清空并重建。")

    # 2. 遍历源目录
    copied_files = 0
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".md"):
                source_path = os.path.join(root, file)
                
                try:
                    # 3. 读取frontmatter
                    with open(source_path, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                        
                        # 4. 检查 `publish: true`
                        if post.get('publish') is True:
                            # 计算相对路径，以保持目录结构
                            relative_path = os.path.relpath(source_path, source_dir)
                            destination_path = os.path.join(target_dir, relative_path)
                            
                            # 创建目标子目录
                            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                            
                            # 复制文件
                            shutil.copy2(source_path, destination_path)
                            print(f"已复制: {relative_path}")
                            copied_files += 1

                except Exception as e:
                    # 忽略无法解析的文件，例如模板文件中的 <% ... %>
                    print(f"跳过文件（可能为模板或格式错误）: {source_path}，原因: {e}")

    print(f"--- 同步任务完成 ---")
    print(f"总计复制了 {copied_files} 个已标记为发布的笔记。")


if __name__ == "__main__":
    sync_notes()
