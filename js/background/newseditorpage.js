$("#save").on("click",function () {
    var id=$("#id").val()
    var title=$("#title").val()
    var brief=$("#brief").val()
    var author=$("#author").val()
    var content=$("#content").val()
    var type=$("#typeselect .selectvalue").attr("value")

    $.post("newseditor",{
        id:id,
        title:title,
        brief:brief,
        author:author,
        content:content,
        type:type,
    },function (data) {
        if(data.res==0){
            $("#id").val(data.id)
            $('.notifications.top-left').notify({
                message: { text: title+' 已保存' }
              }).show();
        }
    },"json")
})

$("#typeselect .dropdown-menu a").on("click",function () {
    var sel=$(this)
    var dd=sel.closest(".dropdown")
    var value=dd.find(".selectvalue")
    value.attr("value",sel.text())
    value.text(sel.text())
})
