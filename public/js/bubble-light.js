// static/js/bubble-light.js (新版：驱动线性扫光)
document.addEventListener('DOMContentLoaded', () => {
    const bubble = document.getElementById('chat-bubble');

    if (!bubble) {
        return;
    }

    bubble.addEventListener('mousemove', (e) => {
        const rect = bubble.getBoundingClientRect();
        // 计算鼠标在气泡内的横向位置百分比（从 -50% 到 +50%）
        const xPercent = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
        
        // 将这个百分比值传递给 CSS
        bubble.style.setProperty('--mouse-x-pos', xPercent);
    });
});