#coding:utf-8
import weixin.basic
token=weixin.basic.GetAccessToken()
menubody={
    "button":[{
           "name":u"我的产品",
           "sub_button":[
           {
               "type":"view",
               "name":u"我的收益",
               "url":"http://news.wowfantasy.cn/wxauthstart"
            },
               {
                   "type": "view",
                   "name": u"我的提醒",
                   "url": "http://news.wowfantasy.cn/wxauthstart?state=remind"
               },
           ]
    },
        {
            "name": u"我的选择",
            "sub_button": [
                {
                    "type": "view",
                    "name": u"本地银行",
                    "url": "http://news.wowfantasy.cn/wxauthstart?state=myselect"
                },
                {
                    "type": "view",
                    "name": u"专享/循环",
                    "url": "http://jiangwenjing.github.io/qiangena/jijinzhuanxiang.html"
                },
                {
                    "type": "view",
                    "name": u"基金产品",
                    "url": "http://jiangwenjing.github.io/qiangena/jijinchanpin.html"
                },
                {
                    "type": "view",
                    "name": u"外地银行",
                    "url": "http://news.wowfantasy.cn/wxauthstart?state=myselect2"
                },
                {
                    "type": "view",
                    "name": u"我的预约",
                    "url": "http://news.wowfantasy.cn/wxauthstart?state=reserve"
                },
            ]
        },
        {
            "name": u"我的社区",
            "sub_button": [
                {
                    "type": "view",
                    "name": u"达人理财",
                    "url": "http://1.qiangena.applinzi.com/dakafenxiang/share.html"
                },
                {
                    "type": "view",
                    "name": u"银行荐财",
                    "url": "http://1.qiangena.applinzi.com/dakafenxiang/share.html"
                },
                {
                    "type": "view",
                    "name": u"产品讲座",
                    "url": "http://1.qiangena.applinzi.com/dakafenxiang/share.html"
                },
                {
                    "type": "view",
                    "name": u"理财吐槽",
                    "url": "http://1.qiangena.applinzi.com/dakafenxiang/share.html"
                },
                {
                    "type": "view",
                    "name": u"使用说明",
                    "url": "http://jiangwenjing.github.io/qiangena/guide.html"
                },
            ]
        }
    ]
}
weixin.basic.DeleteMemu(token)
weixin.basic.SetMenu(token,menubody)