$(function() {
    $('.tab-content').on().on("click",".change",function () {
        var cpdjbm=$(this).closest("li").attr("cpdjbm")
        window.location.href="/revise?cpdjbm="+cpdjbm
    })
    $('.tab-content li').on("click",function () {
        var cpdjbm=$(this).attr("cpdjbm")
        window.location.href='/profitdetail?cpdjbm='+cpdjbm;
    });

});

