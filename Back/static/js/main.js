/**
 * Created by admin on 2017/9/8.
 */

$('.userinfo').click(function () {
    $("#myModal").modal();
});

$('.xiugai').click(function () {
    $("#UPPassWord").modal();
});

// ifame框架打开页面
var openpage = function (href) {
    $(".addpage").empty();
    var html = '<iframe id="iframe-page-content" src="'+href+'" height="650px"   width="100%"  frameborder="no" border="0" marginwidth="0" marginheight=" 0" scrolling="no" allowtransparency="yes"></iframe>'
    $(".addpage").append(html);
}

//about
$(".addmeu").click(function(){
    var href= $(this).attr("data-href");
    openpage(href);
});

//回帖编辑
$(".doedit").click(function () {
    var id= $(this).attr("id");
    $("#txt_departmentname").val(id);
});

//主题编辑
$(".dotitleedit").click(function () {
    var id= $(this).attr("id");
    $.ajax({
        type: "GET",
        url: '/titled',
        data:{"id":id,},
        dataType: 'json',
        success: function (data) {
            $("#txt_departmentname").val(data.id);
            $("#titlename").val(data.title);
            $("#titlecontent").val(data.content);
        }
    });
});