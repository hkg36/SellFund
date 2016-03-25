#coding:utf-8
import weixin.basic
token=weixin.basic.GetAccessToken()
menubody={
    "button":[{
        "type":"view","name":u"我的产品","url":"http://news.wowfantasy.cn/wxauthstart",
    }]
}
weixin.basic.DeleteMemu(token)
weixin.basic.SetMenu(token,menubody)