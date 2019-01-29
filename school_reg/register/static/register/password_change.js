$(function () {
    function checkPassword() {
        $.ajax({
            url: "/password_online",
        })
            .done(function (data) {
                if (data === '1') {
                    $('#dialog').show();
                }
            });
    }
    checkPassword();
});


