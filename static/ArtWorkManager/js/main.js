//发布任务//

//根据tag和taginfo搜索大版本号
function search_version(object){
    item_id = $(object).attr('id');
    name_str = $('#' + item_id).attr("id");
    value_str = $('#' + item_id).val();
    tag_info = $('#tags').val();
    var objjson = JSON.parse(tag_info);
    if (objjson["group"] != $("#group").val())
    {
        objjson={};
    }
    objjson[name_str] = value_str;
    $('#tags').val(JSON.stringify(objjson));
    var json_str = JSON.stringify(objjson);
    var addhttp;
    if (value_str=="")
    {
        return;
    }
    if (window.XMLHttpRequest)
    {
        addhttp=new XMLHttpRequest();
    }
    else
    {
        addhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    addhttp.onreadystatechange=function()
    {
        if(addhttp.readyState==4 && addhttp.status==200)
        {
            $('#big_version').html(addhttp.responseText);
        }
    }
    addhttp.open('POST', '/plan/search_bv/', true);
    addhttp.send(json_str);
}


//根据group查找tag和taginfo
function search_tag(object){
    group = object.value;
    var xmlhttp;
    if (group == ""){
        $("#tag_info").html("<h4>请选择资源类别</h4>");
        $("#big_version").html('<div class="form-group"><label for="big_version">任务版本号 Big_Version</label><select name="big_version" class="form-control" disabled></select></div>');
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
            search_version(object)
        }
    };
    xmlhttp.open("GET", "/plan/gtt?group_id=" + group, true);
    xmlhttp.send();
}


//跳转到通过审核和未通过审核页面
//function to_audit(str){
//    if (str == "0")
//    {
//        to_url = "/plan/faild_task/"
//    }
//    else if (str == "1")
//    {
//        to_url = "/plan/pass_task/"
//    }
//    var xmlhttp;
//    if (window.XMLHttpRequest){
//        xmlhttp = new XMLHttpRequest();
//    }
//    else{
//        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
//    }
//    xmlhttp.onreadystatechange=function(){
//        if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
//            $("#audit_task").html(xmlhttp.responseText);
//        }
//    };
//    xmlhttp.open("GET", to_url, true);
//    xmlhttp.send();
//}


//搜索资源//

//记录选择的数据,存储为Json格式发送到后台,用于搜索资源
function search_image(object){
    item_id = $(object).attr('id');
    name_str = $('#' + item_id).attr("id");
    value_str = $('#' + item_id).val();
    tag_info = $('#images').val();
    var objjson = JSON.parse(tag_info);
    if (objjson["group"] != $("#group").val())
    {
        objjson={};
    }
    objjson[name_str] = value_str;
    $('#images').val(JSON.stringify(objjson));
    var json_str = JSON.stringify(objjson);
    var addhttp;
    if (value_str=="")
    {
        return;
    }
    if (window.XMLHttpRequest)
    {
        addhttp=new XMLHttpRequest();
    }
    else
    {
        addhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    addhttp.onreadystatechange=function()
    {
        if(addhttp.readyState==4 && addhttp.status==200)
        {
            $('#search_img').html(addhttp.responseText);
        }
    };
    addhttp.open('POST', '/developer/search/', true);
    addhttp.send(json_str);
}

//根据group查找tag和taginfo
function search_gtt(object){
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
            search_image(object)
        }
    };
    xmlhttp.open("GET", "/developer/gtt/?group_id=" + group, true);
    xmlhttp.send();
}



//弹出层上传图片
function showDiv(){
    document.getElementById('popDiv').style.display='block';
    document.getElementById('popIframe').style.display='block';
    document.getElementById('bg').style.display='block';
}
function closeDiv(){
    document.getElementById('popDiv').style.display='none';
    document.getElementById('bg').style.display='none';
    document.getElementById('popIframe').style.display='none';
}

function createXMLHttps(){
    var ret = null;
    try {
        ret = new ActiveXObject('Msxml2.XMLHTTP');
    }
    catch (e){
        try {
            ret = new ActiveXObject('Microsoft.XMLHTTP');
        }
        catch (ee) {
            ret = null;
        }
    }
    if (!ret&&typeof XMLHttpRequest !='undefined')
        ret = new XMLHttpRequest();
    return ret;
}

function AjaxGet(URL){
    showDiv();
    var xmlhttp;
    if (window.XMLHttpRequest){
        xmlhttp = new XMLHttpRequest();
    }
    else{
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.open("Get",URL,true);
    xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status==404){
            document.getElementById("popDiv").innerHTML='读取页面失败,文件'+URL+'不存在!';
        }
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
            document.getElementById("popDiv").innerHTML=xmlhttp.responseText;
        }
    };
    xmlhttp.send(null);
}