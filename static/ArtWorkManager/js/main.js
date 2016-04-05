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
    xmlhttp.open("GET", "/plan/gtt?group_id=" + group,true);
    xmlhttp.send();
}


//搜索资源//

//记录选择的数据,存储为Json格式发送到后台,用于搜索资源
function search_image(object){
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
    addhttp.open('POST', '', true);
    addhttp.send(json_str);
}

//根据group查找tag和taginfo
function group_to_tag(object){
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
    xmlhttp.open("GET", "", true);
    xmlhttp.send();
}



