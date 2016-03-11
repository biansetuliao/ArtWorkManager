//根据group查找tag和taginfo
function search_tag(object){
    group = object.value;
    var xmlhttp;
    if (group == ""){
        $("#tag_info").html("<h4>请选择资源类别</h4>");
        return;
    }
    if (window.XMLHttpRequest){
        xmlhttp = new XMLHttpRequest();
    }
    else{
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function(){
        if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
            $("#tag_info").html(xmlhttp.responseText);
        }
    };
    xmlhttp.open("GET", "");
    xmlhttp.send();
}
