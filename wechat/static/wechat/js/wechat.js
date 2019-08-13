$(document).ready(function() {
    var options = {
        success: function(data) {
            $('#id_times').html(data.times);
            //$.get("/wechat/result?page=1",function(data,status){
            //    $('#newsList').html(data);
            //});
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
