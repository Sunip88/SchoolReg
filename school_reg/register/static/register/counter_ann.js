$(function () {
    function refreshCounter() {
        $.ajax({
            url: "/announcements_online",
        })
            .done(function (data) {
                let msg = $("#msg_counter");
                msg.text(data);
                if (data !== '0') {
                    msg.parent().css('font-weight', 'bold')
                } else {
                    msg.parent().css('font-weight', 'normal')
                }
            });
    }
    setInterval(refreshCounter, 15000);
    refreshCounter();
});


