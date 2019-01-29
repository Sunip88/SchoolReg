$(function () {
    var checkall = $('#check_all');
    checkall.change(function () {
        let allcheckboxes = $(".students");
        if ($(this).is(":checked")) {
            allcheckboxes.prop('checked', true)
        } else {
            allcheckboxes.prop('checked', false)
        }
    })
});