$(function () {
    var oNum = document.getElementById('code');
    var oDiv = document.getElementById('list');
    oNum.onfocus = function () {
        oDiv.style.display = 'block';
    };
    oNum.onblur = function () {
        oDiv.style.display = 'none';
    }
    $("#addone").on("click",function () {
        var cpdjbm=$("#code").val()
        var value=$("#value").val()
        var today = new Date();
        var time=today.getFullYear()+"-"+(today.getMonth() + 1)+"-"+today.getDate()
        $.post("",{cpdjbm:cpdjbm,value:value,time:time},function (res) {
            alert(res)
        })
    })
    $("#id").bind("input propertychange",function () {
        $(".continue").val($(this).val())
    })
})
