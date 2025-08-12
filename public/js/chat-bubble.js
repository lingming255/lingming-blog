// static/js/chat-bubble.js
document.addEventListener('DOMContentLoaded', () => {
    const bubble = document.getElementById('chat-bubble');
    const bubbleText = document.getElementById('chat-bubble-text');

    if (!bubble || !bubbleText) {
        return;
    }

    // 在这里添加您想展示的句子
    const quotes = [
        "今天也是充满希望的一天！",
        "我会在墙外插上一束玫瑰。",
        "你看到我的小熊了吗？",
        "读万卷书，行万里路。",
        "愿你眼里的星星，永远亮晶晶。",
        "保持好奇，继续探索。",
        "干饭 / 睡觉 / 瑟瑟"
    ];

    function setNewQuote() {
        const randomIndex = Math.floor(Math.random() * quotes.length);
        bubbleText.textContent = quotes[randomIndex];
    }

    // 为气泡添加点击事件
    bubble.addEventListener('click', setNewQuote);

    // 设置初始文字
    setNewQuote();
});