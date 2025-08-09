(function() {
    // 【升级点 1】: 创建一个“定时器句柄”变量，用于管理我们的定时器。
    // 使用 let 是因为它未来会被修改。
    let visibilityChangeTimer = null; 

    const originalTitle = document.title;
    const awayMessage = "别走嘛QAQ";
    const welcomeMessage = "欢迎QWQ";
    
    document.addEventListener('visibilitychange', function() {
        // 【升级点 2】: 在执行任何新操作之前，先无条件清除掉所有旧的、待执行的定时器。
        // 这就像在发布新命令前，先撤销所有旧命令，保证指令的唯一性。
        if (visibilityChangeTimer) {
            clearTimeout(visibilityChangeTimer);
        }

        if (document.visibilityState === 'hidden') {
            // 当用户离开时，我们只需要改变标题，不需要设置新的定时器。
            document.title = awayMessage;

            visibilityChangeTimer = setTimeout(function() {
                document.title = originalTitle;
            }, 6000);
        } else {
            // 当用户返回时...
            document.title = welcomeMessage;
            
            // 【升级点 3】: 设置新的“恢复”定时器，并把它的句柄/ID存入我们的管理变量中。
            visibilityChangeTimer = setTimeout(function() {
                document.title = originalTitle;
            }, 3000);
        }
    });
})();