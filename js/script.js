$(function() {
    var tabTit = $('.tab-title li');
    var tabCon = $('.tab-content div');
    for (var i = 0; i < tabTit.length; i++) {
        tabTit[i].index = i;
        tabTit[i].onclick = function() {
            for (var j = 0; j < tabTit.length; j++) {
                tabTit[j].className = '';
                tabCon[j].style.display = 'none';
            }
            this.className = 'select';
            tabCon[this.index].style.display = 'block';
        }
    }

    $('.tab-content').on("click","li",function () {
        var cpdjbm=$(this).attr("cpdjbm")
        window.location.href='/profitdetail?cpdjbm='+cpdjbm;
    });
});

