#coding:utf-8
import weixin.basic
token=weixin.basic.GetAccessToken()
menubody={
    "button":[{
           "name":u"我的收益",
           "sub_button":[
           {
               "type":"view",
               "name":u"我的产品",
               "url":"http://news.wowfantasy.cn/wxauthstart"
            },
               {
                   "type": "view",
                   "name": u"我的提醒",
                   "url": "http://news.wowfantasy.cn/wxauthstart"
               },
           ]
    },
        {
            "name": u"我的选择",
            "sub_button": [
                {
                    "type": "view",
                    "name": u"我的银行",
                    "url": "http://news.wowfantasy.cn/wxauthstart"
                },
                {
                    "type": "view",
                    "name": u"我的预约",
                    "url": "http://news.wowfantasy.cn/wxauthstart"
                },
                {
                    "type": "view",
                    "name": u"我的关注",
                    "url": "http://news.wowfantasy.cn/wxauthstart"
                },
            ]
        },
        {
            "name": u"我的社区",
            "sub_button": [
                {
                    "type": "view",
                    "name": u"大咖分享",
                    "url": "http://1.qiangena.applinzi.com/dakafenxiang/share.html"
                },
                {
                    "type": "view",
                    "name": u"银行荐财",
                    "url": "http://1.qiangena.applinzi.com/dakafenxiang/share.html"
                },
                {
                    "type": "view",
                    "name": u"产品预判",
                    "url": "http://1.qiangena.applinzi.com/dakafenxiang/share.html"
                },
                {
                    "type": "view",
                    "name": u"理财体验",
                    "url": "http://1.qiangena.applinzi.com/dakafenxiang/share.html"
                },
                {
                    "type": "view",
                    "name": u"线下讲座",
                    "url": "http://1.qiangena.applinzi.com/dakafenxiang/share.html"
                },
            ]
        }
    ]
}
weixin.basic.DeleteMemu(token)
weixin.basic.SetMenu(token,menubody)