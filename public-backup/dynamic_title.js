(function() {
    const originalTitle = document.title;
    const awayMessage = "别走嘛QAQ";
    const welcomeMessage = "欢迎QWQ";
    
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'hidden') {
            document.title = awayMessage;
        } else {
            document.title = welcomeMessage;
            setTimeout(function() {
                document.title = originalTitle;
            }, 2000);
        }
    });
})();