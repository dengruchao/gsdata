$(document).ready(function() {
    var options = {
        //target: '#output2',
        success: function(data) {
            if(data.error_code == 2) {
            }
        }
    };
    $('#loginForm').on('submit', function(e) {
        e.preventDefault(); // <-- important
        $(this).ajaxSubmit(options);
    });
});
