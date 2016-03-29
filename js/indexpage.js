var $$ = Dom7;
var debugitem
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

function transDate(proddata){
    var copy={}
    copy.mjqsrq=new Date(proddata.mjqsrq)
    copy.mjjsrq=new Date(proddata.mjjsrq)
    copy.cpqsrq=new Date(proddata.cpqsrq)
    copy.cpyjzzrq=new Date(proddata.cpyjzzrq)
    return copy
}
function calcProfit(product){
    var now=new Date()
    var dates=transDate(product)
    var buydate=new Date(product.buy_value.date.replace(/-/g,"/"))
    var buyvalue=product.buy_value.value
    var holdspan=Math.floor((now-(buydate-dates.cpqsrq>0?buydate:dates.cpqsrq))/(1000*60*60*24))
    if(holdspan<0){
        return 0
    }
    var cpspan=Math.floor((dates.cpyjzzrq-dates.cpqsrq)/(1000*60*60*24))
    var aveprofit=(parseFloat(product.yjkhzgnsyl)+parseFloat(product.yjkhzdnsyl))/2
    return (buyvalue*holdspan/cpspan*aveprofit/100).toFixed(2)
}
app.onPageInit("page_main", function (page) {
    var mySearchbar
    var search_order="-yjkhzgnsyl"

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
                    list[i].linkinfo = packjson(list[i])
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
    goSearch()
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
        var profits2=""
        var allprofit=0
        now=new Date()
        $$.each(products,function(i,v){
            var date=transDate(v)

            var prf=calcProfit(v)
            allprofit+=parseFloat(prf)
            var dayrem=(date.cpyjzzrq-now)/(1000*60*60*24)
            if(dayrem<10)
                profits2+=tpl.format(packjson(v),v.cpms, prf)
            else
                profits+=tpl.format(packjson(v),v.cpms, prf)
        })
        $$("#mainpagelist").html('<li class="item-divider">我的理财收益</li>'+profits+'<li class="item-divider">即将到期的理财产品</li>'+profits2)
        $$("[data-page=page_main] [data=allprofit]").text(allprofit.toFixed(2))
        $$("[data-page=page_main] [data=productcount]").text(products.length)
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

$$(document).on('pageReinit pageInit', '.page[data-page="productdetail"]', function (e) {
    var page = e.detail.page;
    var proddata = unpackjson(page.query.info)
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
    $$("#addtomyproduct [datatype=cpms]").text(proddata.cpms)
})

$$(document).on('pageReinit pageInit', '.page[data-page="mydetail"]', function(e){
    var page = e.detail.page;
    var proddata = unpackjson(page.query.info)
    var tpl = $$("#productinfoline").html()
    var htmlstr = '<li class="item-divider">产品明细</li>'
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
    $$(page.container).find("ul[data='detail']").html(htmlstr)
    $$(page.container).find("[data=name]").html(proddata.cpms)

    $$(page.container).find("[data=profit]").text(calcProfit(proddata))
    $$(page.container).find("[data=day]").text(Math.floor((new Date()-new Date(proddata.buy_value.date.replace(/-/g,"/")))/(1000*60*60*24)))
})
$$(document).on('pageInit', '.page[data-page="watchproduct"]', function(e){
    $$('.page[data-page="watchproduct"] .resultlist').on("click","a[act=dounwatch]",function(){
        var btn=$$(this)
        var cpdjbm=btn.attr("data")
        $$.get("/datas/dowatch",{cpdjbm:cpdjbm,remove:1},function(){
            btn.parents("div.card").eq(0).remove()
        })
    })
})
$$(document).on('pageInit pageReinit', '.page[data-page="watchproduct"]', function(e){
    $$.get('/datas/watchprod',function(data){
        var data=JSON.parse(data)
        var tpl=$$("#productwatchcell").html()
        var htmlstr=""
        $$.each(data.list,function(k,v){
            v.linkinfo=packjson(v)
            htmlstr+=tpl.formatO(v)
        })
        $$('.page[data-page="watchproduct"] .resultlist').html(htmlstr)
    })
})
app.init()
$$("#addtomyproduct").on("open",function(){
    $$(this).find("[data-value]").val("")
    $$(this).find("[data-day]").val("")
})
$$("#addtomyproduct .button[data-ok]").on("click", function () {
    var cpdjbm = $$("#addtomyproduct [datatype=cpdjbm]").val()
    var value = $$("#addtomyproduct [data-value]").val()
    var date=$$("#addtomyproduct [data-day]").val()
    $$.post("/datas/recordbuy", {cpdjbm: cpdjbm, value: value,date:date}, function (data) {
    })
    app.closeModal("#addtomyproduct")
})
app.calendar({
    input: '#addtomyproduct [data-day]',
});
var mainView = app.addView('.view-main', {
    dynamicNavbar: true,
    domCache: true
});

