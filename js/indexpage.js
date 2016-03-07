var $$ = Dom7;
var app = new Framework7({
    init: false,
});
function packjson(obj){
    var str = JSON.stringify(obj).replace(/[\u007F-\uFFFF]/g, function (chr) {
                        return "\\u" + ("0000" + chr.charCodeAt(0).toString(16)).substr(-4)
                    })
    return btoa(str)
}
function unpackjson(data){
    return JSON.parse(atob(data))
}
app.onPageInit("page_main", function (page) {
    var mySearchbar
    var search_order

    function goSearch(e) {
        $$.ajax({
            method: "POST",
            url: "/datas/search",
            dataType: "json",
            data: {text: mySearchbar.input.val(), order: search_order},
            success: function (data) {
                var tpl = $$("#prodinfocard").html()
                var htmlstr = ""
                var list = data.list
                for (var i = 0; i < list.length; i++) {
                    var str = JSON.stringify(list[i]).replace(/[\u007F-\uFFFF]/g, function (chr) {
                        return "\\u" + ("0000" + chr.charCodeAt(0).toString(16)).substr(-4)
                    })
                    list[i].linkinfo = btoa(str)
                    htmlstr += tpl.formatO(list[i])
                }
                $$("#tablist .resultlist").html(htmlstr)
            },
            complete: function () {

            }
        })
    }

    mySearchbar = app.searchbar('.searchbar', {
        customSearch: true,
        onSearch: goSearch
    });
    $$(page.container).find("#ordertype").on("click", "a[order]", function (e) {
        var btn = $$(this)
        btn.prevAll().removeClass("active")
        btn.nextAll().removeClass("active")
        btn.addClass("active")
        search_order = btn.attr("order")
        goSearch()
    })
    $$(".pages").on("click", "a[act=dowatch]", function () {
        var watchlink = $$(this)
        $$.get("/datas/dowatch", {cpdjbm: watchlink.attr("data")}, function () {
            watchlink.addClass("active")
        })
    })
    $$.get("/datas/myinfo",function(data){
        data=JSON.parse(data)
        var products=data.list;
        var tpl=$$("#profitinfoline").html()
        var profits=""
        $$.each(products,function(i,v){
            profits+=tpl.format(packjson(v),v.cpms, v.buy_value)
        })
        $$("#mainpagelist").html('<li class="item-divider" id="profitlist">我的理财收益</li>'+profits)
    })
})
$$(document).on('pageInit', '.page[data-page="select_bank"]', function (e) {
    var page = e.detail.page
    $$.getJSON("js/banklist.json", function (data) {
        $$.getJSON("/datas/watchbank", function (sellist) {
            var htmldata = ""
            var tpl = $$("#banklistcell").html()
            for (var i = 0; i < data.length; i++) {
                htmldata += tpl.formatO({
                    bankname: data[i],
                    checked: sellist.indexOf(data[i]) == -1 ? "" : "checked"
                })
            }
            $$("#bankselectlist").html(htmldata)
        })
    })
    $$(page.navbarInnerContainer).find(".save_button").on("click", function () {
        var banks = $$("#bankselectlist input[name='bankselect']:checked")
        var banklist = []
        for (var i = 0; i < banks.length; i++) {
            banklist.push($$(banks[i]).val())
        }
        $$.ajax({
            method: "POST",
            url: "/datas/watchbank",
            dataType: "json",
            contentType: "text/json",
            processData: false,
            data: JSON.stringify(banklist),
            success: function (data) {
            },
            complete: function () {

            }
        })
    })
})
function InitProductDetail(e) {
    var page = e.detail.page;
    var proddata = JSON.parse(atob(page.query.info))
    var tpl = $$("#productinfoline").html()
    var htmlstr = '<li class="item-divider">{0}</li>'.format(proddata.cpms)
    htmlstr += tpl.format("登记编码", proddata.cpdjbm)
    htmlstr += tpl.format("收益类型", proddata.cpsylxms)
    htmlstr += tpl.format("运作模式", proddata.cplxms)
    htmlstr += tpl.format("风险等级", proddata.fxdjms)
    htmlstr += tpl.format("起售金额", proddata.qdxsje + "元")
    htmlstr += tpl.format("期限类型", proddata.qxms)
    htmlstr += tpl.format("实际天数", proddata.cpqx + "天")
    htmlstr += tpl.format("发行机构", proddata.fxjgms)
    htmlstr += tpl.format("预期最高收益率", proddata.yjkhzgnsyl)
    htmlstr += tpl.format("预期最低收益率", proddata.yjkhzdnsyl)
    htmlstr += tpl.format("初始净值", proddata.csjz)
    htmlstr += tpl.format("本期净值", proddata.bqjz)
    htmlstr += tpl.format("截止到", proddata.cpyjzzrq)
    htmlstr += tpl.format("产品净值", proddata.cpjz)
    htmlstr += tpl.format("募集起始日期", proddata.mjqsrq)
    htmlstr += tpl.format("募集结束日期", proddata.mjjsrq)
    htmlstr += tpl.format("产品起始日期", proddata.cpqsrq)
    htmlstr += tpl.format("产品结束日期", proddata.cpyjzzrq)
    $$(page.container).find(".infodata").html(htmlstr)

    $$("#addtomyproduct [datatype=cpdjbm]").val(proddata.cpdjbm)
}
$$(document).on('pageReinit pageInit', '.page[data-page="productdetail"]', InitProductDetail)

app.init()

$$("#addtomyproduct .button").on("click", function () {
    var cpdjbm = $$("#addtomyproduct [datatype=cpdjbm]").val()
    var value = $$("#addtomyproduct [data-value]").val()
    $$.post("/datas/recordbuy", {cpdjbm: cpdjbm, value: value}, function (data) {
    })
    app.closeModal("#addtomyproduct")
})
var mainView = app.addView('.view-main', {
    dynamicNavbar: true,
    domCache: true
});

