$(function() {
    $('.tab-content').on("click","li",function () {
        var cpdjbm=$(this).attr("cpdjbm")
        window.location.href='/profitdetail?cpdjbm='+cpdjbm;
    });
});

