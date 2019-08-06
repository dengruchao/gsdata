$(document).ready(function() {
    var options = {
        success: function(data) {
            if(data.error_code != 0) {
                $('#id_loginModal').html(data.msg)
                $('#loginModal').modal('show');
            } else {
                window.location.href="/";
            }
        }
    };
    $('#loginForm').on('submit', function(e) {
        e.preventDefault(); // <-- important
        $(this).ajaxSubmit(options);
    });
});
