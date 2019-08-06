$(document).ready(function() {
    var options = {
        success: function(data) {
            $('#id_times').html(data.times);
        }
    };
    $('#searchForm').on('submit', function(e) {
        e.preventDefault(); // <-- important
        $(this).ajaxSubmit(options);
    });
});
