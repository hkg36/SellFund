import weixin.basic
import database
import json

def GetLastNews():
    data=database.memclient.get("weixin.lastnews")
    try:
        if data:
            return json.loads(data)
    except:
        pass
    medias = weixin.basic.GetMediaList("news")
    if len(medias):
        data=medias[0]
        database.memclient.set("weixin.lastnews",json.dumps(data),3600*24)
        return data
    return None

if __name__ == '__main__' :
    print json.dumps(GetLastNews(),ensure_ascii=False)