$(function () {
   /* $("#code").on("focus",function () {
        $("#list").show()
    })
    $("#code").on("blur",function () {
        $("#list").hide()
    })*/
    $("#addone").on("click",function () {
        var cpdjbm=$("#code").val()
        var value=$("#value").val()
        var today = new Date();
        var time=today.getFullYear()+"-"+(today.getMonth() + 1)+"-"+today.getDate()
        $.post("/guide",{cpdjbm:cpdjbm,value:value,time:time},function (res) {
            alert(res)
        })
    })
    $("#code").on("input propertychange",function () {
        
    })
})
