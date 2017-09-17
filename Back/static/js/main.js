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
    var html = '<iframe id="iframe-page-content" src="'+href+'" width="100%"  frameborder="no" border="0" marginwidth="0" marginheight=" 0" scrolling="no" allowtransparency="yes"></iframe>'
    $(".addpage").append(html);
    var ifm= document.getElementById("iframe-page-content");
    ifm.height=document.documentElement.clientHeight+100;
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

var pageconf=1;

// 回复搜索按钮
$('.btn-primary').on('click',function () {
    var Npage = 1;
    id=document.getElementById("id").value;
    title=document.getElementById("title").value;
    content_user=document.getElementById("username").value;
    Refreshs(pageconf,Npage,id,title,content_user)
});


var Npage = 1;
// pagenum 总页数 page 当前页数
var Page = function (pagenum,page) {
    // 向上取整,有小数就整数部分加1,计算总页数
    var temp = Math.ceil(pagenum/10);
    if (temp<7){
        var startpg = 1;
        var endpg = temp;
    };
    if (temp>=7){
        if (page<4){
            var startpg = 1
            var endpg = 7
            }
        if (page>=4){
            if ((page+3)>temp){
                var startpg = temp-6
                var endpg = temp
            }
            else{
                var startpg = page-3
                var endpg = page+3
                }
        }
    };
    var  pgup = page - 1
    var  pgdn = page + 1

    if (pgup<=0){
       var  pgup = 1
    }
    if (pgdn>=temp) {
        var  pgdn = temp
    }
    var endpg = endpg+1;

    if (temp>1){
        var pagedata = '<ul class="pagination pagination-sm jsonadd" ><li><a href="javascript:;" onclick="Getid(this);" name="'+pgup+'">&laquo;</a></li>'
        for (var i=startpg;i<endpg;i++) {
            if (page == i){
                pagedata += '<li class ="active"><a href="javascript:;" onclick="Getid(this);" name="'+i+'">'+i+'</a></li>'
            }else {
                 pagedata += '<li><a href="javascript:" onclick="Getid(this);" name="'+i+'">'+i+'</a></li>'
            }
        }
        pagedata += '<li><a href="javascript:;" onclick="Getid(this);" name="'+pgdn+'">&raquo;</a></li></ul>'
        $(".pagedata").append(pagedata);

    }else {
        return
    }
}

// pageconf url后面的参数 Npage 访问的页数
var Refreshs = function (pageconf,Npage,id,title,content_user) {
    var url = '/huifu/'+pageconf;
    var a = Npage*10
    if(Npage==1){
        var startNum = 0;
        var endNum = a-1;
    }else {
        var startNum = a-10;
        var endNum = a-1;
    }
    $.ajax({
        type: "POST",
        url: url,
        data: {id: id, title: title, content_user: content_user},
        dataType: 'json',
        success: function (data) {
            $(".jsonadd").remove();
            if(data==""){
                $(".huifudata").append("<tr class='jsonadd'><td colspan=6>暂无数据</td></tr>")
            }

            var dataLenth = data.length;
            if(endNum>=dataLenth){
                 endNum = dataLenth;
            }else {
                endNum = endNum+1;
            }
            var htmldata = ''

            for(var i=startNum;i<endNum;i++){
                i = parseInt(i);
                id = data[i]["id"]
                content_user = data[i]["content_user"]
                content = data[i]["content"].substring(0,15)
                fbtime = data[i]["fbtime"]
                title = data[i]["title"]
                htmldata +='<tr class="jsonadd"><td>'+id+'</td><td>'+content_user+'</td><td>'+content+'</td><td>'+fbtime+'</td><td>'+title+'</td><td><a href="#" class="doedit" id="'+id+'"data-toggle="modal" data-target="#myModal">编辑</a>&nbsp;&nbsp;<a href="#">删除</a></td></tr>'
            }

            htmldata += '<tr class="jsonadd"><td colspan=6></td></tr>'

            $(".huifudata").append(htmldata);
            Page(dataLenth,Npage);

            $(".doedit").click(function () {
                var id= $(this).attr("id");
                $("#txt_departmentname").val(id);
            });
        }
    });
}

// 翻页操作
function Getid(obj){
    var value=(obj.name);
    Npage = value
    Refreshs(pageconf,Npage,id,title,content_user)
}