$(document).ready(function () {
    $('.checkbox').click(function () {
        $.ajax({
            url: "/list",
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                activity: "check",
                id: $(this).val()
            }),
            success: function () {
                window.location.reload()
            }
        })
    })
    $('#submit').click(function () {
        $.ajax({
            url: "/list",
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                activity: "add",
                content: $('.input').val(),
                id: $('.value').val()
            }),
            success: function () {
                window.location.reload()
            }
        })
    })
})
