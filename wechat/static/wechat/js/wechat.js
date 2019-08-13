$(document).ready(function() {
    var options = {
        beforeSend: function(data) {
            $("#loadingModal").modal({backdrop: 'static', keyboard: false});
        },
        success: function(data) {
            $("#loadingModal").modal('hide');
            $('#id_times').html(data.times);
            get_result(1);
        }
    };
    $('#searchForm').on('submit', function(e) {
        e.preventDefault(); // <-- important
        $(this).ajaxSubmit(options);
    });
});

function get_result(page) {
    $.get("/wechat/result?page="+page,function(data,status){
        $('#newsList').html(data);
    });
}

function sort_result(obj, by) {
    $('#sortDropdownMenu').text(obj.text);
    $.get("/wechat/sort_result?by="+by,function(data,status){
        get_result(1);
    });
}
