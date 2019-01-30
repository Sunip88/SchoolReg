$(function () {
    var delete_btn = $("#delete_btn");
    delete_btn.on("click", function () {
        var deleted_art = $(this).parent().parent().parent();
        let data = $(this).data('one');
        let token = $("#ann_form").find('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
             type:"POST",
             url:"/announcements/",
             data: {
                    'approved': data,
                    csrfmiddlewaretoken: token},
            success: function () {
                deleted_art.hide()
                }

            });

    });
    var read_btn = $("#read_btn");
    read_btn.on("click", function () {
        var read_art = $(this).siblings("p");
        var read_btn = $(this)
        let data = $(this).data('one');
        let token = $("#ann_form").find('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
             type:"POST",
             url:"/announcements/",
             data: {
                    'approved': data,
                    csrfmiddlewaretoken: token},
            success: function () {
                read_art.removeClass("font-weight-bold");
                console.log($(this));
                read_btn.hide()
                }

            });

    });
});
