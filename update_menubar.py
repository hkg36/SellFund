#coding:utf-8
import weixin.basic
token=weixin.basic.GetAccessToken()
menubody={
    "button":[{
        "type":"view","name":u"我的产品","url":"http://news.wowfantasy.cn/wxauthstart",
    },{"type":"view","name":u"使用说明","url":"http://news.wowfantasy.cn/guide"}]
}
weixin.basic.DeleteMemu(token)
weixin.basic.SetMenu(token,menubody)