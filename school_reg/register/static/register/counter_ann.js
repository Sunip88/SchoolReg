$(function () {
    function refreshCounter() {
        $.ajax({
            url: "/announcements_online",
        })
            .done(function (data) {
                let msg = $("#msg_counter");
                msg.text(data);
                if (data !== 2) {
                    msg.parent().css('font-weight', 'Bold')
                }
            });
    }
    setInterval(refreshCounter, 15000);
    refreshCounter();
});


