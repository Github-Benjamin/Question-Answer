/**
 * Created by admin on 2017/9/8.
 */

// Ajax 分页处理逻辑

var test = window.location.href;
pageconf = test.split("/")[4];
var Npage = 1;

// pagenum 总页数 page 当前页数
var Page = function (pagenum,page) {

    // 向上取整,有小数就整数部分加1,计算总页数
    var temp = Math.ceil(pagenum/5);
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
        $(".content-box").append(pagedata);
    }else {
        return
    }

}

// pageconf url后面的参数 Npage 访问的页数
var Refreshs = function (pageconf,Npage) {
    var url = '/questiondata/'+pageconf;
    var a = Npage*5
    if(Npage==1){
        var startNum = 0;
        var endNum = a-1;
    }else {
        var startNum = a-5;
        var endNum = a-1;
    }

    $.ajax({
        type: "GET",
        url: url,
        dataType:'json',
        success: function(data){

            if(data==""){
                $(".content-box").append("<div style='height: 15px'></div><h4>&nbsp;&nbsp;&nbsp;&nbsp;该问题还没有任何用人回答，小哥哥、小姐姐们回复一个呗！(⊙o⊙)…</h4>");
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
                content = data[i]["content"]
                user = data[i]["content_user"]
                fbtime = data[i]["fbtime"]
                htmldata += '<div class="jsonadd"><br>&nbsp;&nbsp;&nbsp;&nbsp;'+user+'&nbsp;&nbsp;'+fbtime+'<br>&nbsp;&nbsp;&nbsp;&nbsp;内容： '+ content+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:;" style="text-decoration:none" class="clickzan">点赞（10）</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:;"  style="text-decoration:none" class="clickhuifu">回复</a><br></div>'
            }
            $(".jsonadd").remove();
            $(".content-box").append(htmldata);
            Page(dataLenth,Npage);

            $(".clickzan").click(function () {
                alert("点赞功能尚未开发");
            });

            $(".clickhuifu").click(function () {
                alert("叠楼功能尚未开发");
            });
        }
    });
}

Refreshs(pageconf,1);

function Getid(obj){
    var value=(obj.name);
    Npage = value
    Refreshs(pageconf,Npage);
}


