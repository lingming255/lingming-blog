// custom-scripts.js (V2 - 带有诊断日志的调试版本)

document.addEventListener('DOMContentLoaded', () => {
    
    console.log("--- [诊断日志] 页面加载完成 (DOMContentLoaded)，开始执行自定义脚本 ---");

    // --- 模块一：聊天气泡逻辑 ---
    console.log("[模块一] 正在初始化聊天气泡...");
    const chatBubble = document.getElementById('chat-bubble');
    console.log("  [诊断] 查找 #chat-bubble 元素:", chatBubble ? "成功找到" : "失败，为 null");

    if (chatBubble) {
        const chatTextElement = chatBubble.querySelector('p');
        console.log("  [诊断] 在气泡内查找 <p> 标签:", chatTextElement ? "成功找到" : "失败，为 null");

        if (chatTextElement) {
            console.log("  [诊断] 气泡和文本元素均已就绪，准备设置点击事件...");
            const quotes = [
                "今天也是充满希望的一天！", "我会在墙外插上一束玫瑰", "你看到我的小熊了吗？",
                "读万卷书，行万里路", "随意破坏、调整，这就是学习的方式", "保持好奇，继续探索",
                "干饭 / 睡觉 / 瑟瑟", "生命偶然，体验至上", "没有人知道",
                "欢迎来到LingMing的小世界", "你知道可以在地址栏里访问/test吗", "Run,don't look back",
                "什么样的结局才配的上这一路的颠沛流离", "我是一个冷笑话","奇迹将会发生",
            ];

            const setNewQuote = () => {
                const randomIndex = Math.floor(Math.random() * quotes.length);
                const newQuote = quotes[randomIndex];
                chatTextElement.textContent = newQuote;
                console.log(`  [动作] 点击事件触发！已将文本设置为: "${newQuote}"`);
            }

            chatBubble.addEventListener('click', setNewQuote);
            console.log("  [诊断] 点击事件已成功绑定。");
            
            setNewQuote(); // 初始化
        } else {
            console.error("  [错误] 未能在 #chat-bubble 内部找到 <p> 标签来显示文字。请检查你的 HTML 结构。");
        }
    } else {
        console.error("  [错误] 未能找到 ID 为 'chat-bubble' 的元素。请检查你的 HTML 结构或模板文件。");
    }

    // --- 模块二：页面标题切换逻辑 ---
    console.log("\n[模块二] 正在初始化页面标题切换逻辑...");
    let visibilityChangeTimer = null; 
    const originalTitle = document.title;
    console.log(`  [诊断] 原始页面标题为: "${originalTitle}"`);
    const awayMessage = "别走嘛QAQ";
    const welcomeMessage = "欢迎QWQ";
    
    document.addEventListener('visibilitychange', () => {
        console.log(`  [动作] 页面可见性发生变化，当前状态: ${document.visibilityState}`);
        if (visibilityChangeTimer) {
            clearTimeout(visibilityChangeTimer);
            console.log("    [诊断] 已清除旧的定时器。");
        }

        if (document.visibilityState === 'hidden') {
            document.title = awayMessage;
            console.log(`    [诊断] 页面已隐藏，标题已设置为: "${awayMessage}"`);
        } else {
            document.title = welcomeMessage;
            console.log(`    [诊断] 页面已恢复可见，标题已设置为: "${welcomeMessage}"`);
            visibilityChangeTimer = setTimeout(() => {
                document.title = originalTitle;
                console.log(`    [动作] 3秒后，标题已恢复为: "${originalTitle}"`);
            }, 3000);
            console.log("    [诊断] 已设置新的3秒恢复定时器。");
        }
    });
    console.log("[模块二] 页面标题切换逻辑已成功初始化。");
});