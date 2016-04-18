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
    var cpspan=360//Math.floor((dates.cpyjzzrq-dates.cpqsrq)/(1000*60*60*24))
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
    $$(page.container).find("#tablist").on("show",function () {
        if($$(this).prop("inited"))
            return
        $$(this).prop("inited","ok")
        goSearch()
    })
    $$(page.container).find("#ordertype").on("click", "a[order]", function (e) {
        var btn = $$(this)
        btn.prevAll().removeClass("active")
        btn.nextAll().removeClass("active")
        btn.addClass("active")
        search_order = btn.attr("order")
        goSearch()
    })
    function reflashMyInfo() {
        $$.get("/datas/myinfo",function(data){
            data=JSON.parse(data)
            var products=data.list;
            var tpl=$$("#profitinfoline").html()
            var tpl2=$$("#aboutfinishline").html()
            var profits=""
            var profits2=""
            var allprofit=0
            var now=new Date()
            $$.each(products,function(i,v){
                var date=transDate(v)

                var prf=calcProfit(v)
                allprofit+=parseFloat(prf)
                var dayrem=(date.cpyjzzrq-now)/(1000*60*60*24)
                if(dayrem<14)
                    profits2+=tpl2.format(packjson(v),v.cpms, prf,(dayrem>0?dayrem:0).toFixed(0))
                else
                    profits+=tpl.format(packjson(v),v.cpms, prf)
            })
            tpl=$$("#watchinfoline").html()
            var watchs=""
            $$.each(data.watch,function (i,v) {
                watchs+=tpl.format(packjson(v),v.cpms,v.fxjgms)
            })
            $$("#mainpagelist").html('<li class="item-divider">我的理财收益</li>'+profits+'<li class="item-divider">即将到期的理财产品</li>'+profits2
            +'<li class="item-divider">我预约的产品</li>'+watchs)
            $$("[data-page=page_main] [data=allprofit]").text(allprofit.toFixed(2))
            $$("[data-page=page_main] [data=productcount]").text(products.length)
        })
    }
    reflashMyInfo()
    $$(page.container).find("#tabhome .reflashbn").on("click",function () {
        reflashMyInfo()
    })

    function getNews() {
        var type=$$(page.container).find("#tabcommunity .typelist a.active").text()
        $$.post('/datas/newslist',{type:type},function (data) {
            data=JSON.parse(data)
            var tpl=$$("#newsline").html()
            var htmlstr=""
            $$.each(data.news,function (k,v) {
                htmlstr+=tpl.formatO(v)
            })
            $$("#tabcommunity .newslist .nline").remove()
            $$(htmlstr).insertAfter("#tabcommunity .newslist .list-group-title")
        })
    }
    $$(page.container).find("#tabcommunity").on("show",function () {
        if($$(this).prop("inited"))
            return
        $$(this).prop("inited","ok")
        getNews()
    })
    $$(page.container).find("#tabcommunity .typelist").on("click","a:not(.active)",function () {
        $$(this).nextAll().removeClass("active")
        $$(this).prevAll().removeClass("active")
        $$(this).addClass("active")
        getNews()
    })
})
$$(document).on('pageInit', '.page[data-page="select_bank"]', function (e) {
    var page = e.detail.page
    //$$.getJSON("js/banklist.json", function (data) {
    data=["中国建设银行","中国工商银行","中国农业银行","中国银行","交通银行","招商银行","中国邮政储蓄银行","北京银行",
        "中信银行","光大银行","上海浦东发展银行","广东发展银行","平安银行","中国民生银行","华夏银行","兴业银行","江苏银行",
        "南京银行","浙商银行","杭州银行","宁波银行","上海银行","锦州银行","盛京银行","恒生银行","大连银行","厦门国际银行","北京农村商业银行"]
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
    //})
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
                page.view.router.back()
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
    //htmlstr += tpl.format("收益类型", proddata.cpsylxms)
    //htmlstr += tpl.format("运作模式", proddata.cplxms)
    htmlstr += tpl.format("风险等级", proddata.fxdjms)
    htmlstr += tpl.format("起售金额", proddata.qdxsje + "元")
    //htmlstr += tpl.format("期限类型", proddata.qxms)
    htmlstr += tpl.format("实际天数", proddata.cpqx + "天")
    htmlstr += tpl.format("发行机构", proddata.fxjgms)
    htmlstr += tpl.format("预期最高收益率", proddata.yjkhzgnsyl)
    htmlstr += tpl.format("预期最低收益率", proddata.yjkhzdnsyl)
   // htmlstr += tpl.format("初始净值", proddata.csjz)
    //htmlstr += tpl.format("本期净值", proddata.bqjz)
    //htmlstr += tpl.format("截止到", proddata.cpyjzzrq)
   // htmlstr += tpl.format("产品净值", proddata.cpjz)
    htmlstr += tpl.format("募集起始日期", proddata.mjqsrq)
    htmlstr += tpl.format("募集结束日期", proddata.mjjsrq)
    htmlstr += tpl.format("产品起始日期", proddata.cpqsrq)
    htmlstr += tpl.format("产品结束日期", proddata.cpyjzzrq)
    htmlstr+='<a href="#bankbranch" class="item-link">'+
        '<div class="item-content">'+
        '<div class="item-inner"><div class="item-title">点击查看该银行附近网点</div></div>'+
        '</div>'+
        '</a>'
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
    //htmlstr += tpl.format("收益类型", proddata.cpsylxms)
    //htmlstr += tpl.format("运作模式", proddata.cplxms)
    //htmlstr += tpl.format("风险等级", proddata.fxdjms)
    //htmlstr += tpl.format("起售金额", proddata.qdxsje + "元")
    //htmlstr += tpl.format("期限类型", proddata.qxms)
    htmlstr += tpl.format("实际天数", proddata.cpqx + "天")
    htmlstr += tpl.format("发行机构", proddata.fxjgms)
    htmlstr += tpl.format("预期最高收益率", proddata.yjkhzgnsyl)
    htmlstr += tpl.format("预期最低收益率", proddata.yjkhzdnsyl)
    //htmlstr += tpl.format("初始净值", proddata.csjz)
    //htmlstr += tpl.format("本期净值", proddata.bqjz)
    //htmlstr += tpl.format("截止到", proddata.cpyjzzrq)
    //htmlstr += tpl.format("产品净值", proddata.cpjz)
    //htmlstr += tpl.format("募集起始日期", proddata.mjqsrq)
    //htmlstr += tpl.format("募集结束日期", proddata.mjjsrq)
    htmlstr += tpl.format("产品起始日期", proddata.cpqsrq)
    htmlstr += tpl.format("产品结束日期", proddata.cpyjzzrq)
    $$(page.container).find("ul[data='detail']").html(htmlstr)
    $$(page.container).find("[data=name]").html(proddata.cpms)

    var now=new Date()
    var date=transDate(proddata)
    var dayrem=(date.cpyjzzrq-now)/(1000*60*60*24)
    if(dayrem<0)
        dayrem=0
    $$(page.container).find("[data=base]").text(proddata.buy_value.value)
    $$(page.container).find("[data=profit]").text(calcProfit(proddata))
    $$(page.container).find("[data=day]").text(Math.floor((new Date()-new Date(proddata.buy_value.date.replace(/-/g,"/")))/(1000*60*60*24)))
    $$(page.container).find("[data=dayleft]").text(Math.floor(dayrem))
    var reservebn=$$(page.container).find("[data=reserve]")
    if(dayrem<14) {
        reservebn.show()
        reservebn.attr("href","#recommendprod?after="+(dayrem==0?now.getTime():date.cpyjzzrq.getTime()))
    }
    else
        reservebn.hide()
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
$$(document).on('pageInit pageReinit', '.page[data-page="news"]', function(e){
    var page = e.detail.page;
    var id=page.query.id
    $$.get("/datas/onenews?id="+id,function (data) {
        data=JSON.parse(data)
        $$(page.container).find(".title").text(data.title)
        $$(page.container).find(".author").text(data.author)
        $$(page.container).find(".time").text(moment(data.time).format("YYYY-MM-DD"))
        $$(page.container).find(".content").html(data.content.replace(/(\r\n)|(\n)/ig,"<br/>"))
    })
})
$$(document).on("pageInit pageReinit",".page[data-page=recommendprod]",function (e) {
    var page = e.detail.page;
    var after=page.query.after
    if(after)
        after=new Date(parseInt(after))
    $$.post("/datas/recommend",{after:after.toISOString()},function (data) {
        data=JSON.parse(data)
        var tpl = $$("#prodinfocard").html()
        var htmlstr = ""
        var list = data.list
        for (var i = 0; i < list.length; i++) {
            list[i].linkinfo = packjson(list[i])
            htmlstr += tpl.formatO(list[i])
        }
        $$(page.container).find(".page-content").html(htmlstr)
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
        app.closeModal("#addtomyproduct")
        mainView.router.back()
        app.alert("可前往我的收益页查看收益哦","录入完成",function () {

        })
    })
})
app.calendar({
    input: '#addtomyproduct [data-day]',
});
var mainView = app.addView('.view-main', {
    dynamicNavbar: true,
    domCache: true
});
$$(document).on("click", ".product-card-small a[act=dowatch]", function () {
        var watchlink = $$(this)
        if(watchlink.hasClass("active"))
            $$.get("/datas/dowatch?remove=1", {cpdjbm: watchlink.attr("data")}, function () {
                watchlink.removeClass("active")
            })
        else
            $$.get("/datas/dowatch", {cpdjbm: watchlink.attr("data")}, function () {
                watchlink.addClass("active")
            })
})
