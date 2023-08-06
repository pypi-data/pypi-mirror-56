import json
import time
import urllib3
import urllib.request
import requests
class AIRobot:
    #Turing API
    def __init__(self,name):
        '''
        初始化函数
            Args:
                name:你自己的名字
        '''
        self.user = str(name)
    TURING_KEY = "2f2326afcdf74041b55c47fb77f66305"
    API_URL = "http://openapi.tuling123.com/openapi/api/v2"
    text = ""
    def Turing_Robot_think(self, text_input):
        req = {
        "perception":
        {
            "inputText":
            {
                "text": text_input
            },

            "selfInfo":
            {
                "location":
                {
                    "city": "天津",
                    "province": "天津",
                    "street": "西康路"
                }
            }
        },
        "userInfo": 
        {
            "apiKey": AIRobot.TURING_KEY,
            "userId": "Hugn"
        }
    }
        # print(req)
        # 将字典格式的req编码为utf8
        req = json.dumps(req).encode('utf8')
        # print(req)

        http_post = urllib.request.Request(AIRobot.API_URL, data=req, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(http_post)
        response_str = response.read().decode('utf8')
        # print(response_str)
        response_dic = json.loads(response_str)
        # print(response_dic)

        intent_code = response_dic['intent']['code']
        results_text = response_dic['results'][0]['values']['text']
        return results_text
    def SiZhi_Robot_think(self, text_input):
        req={
                "spoken": text_input,
                "appid": "8efd35278ee6b77f03b4a77bf0f4fb1d",
                "userid": "Hugn"
            }
        sess = requests.get('https://api.ownthink.com/bot?appid=8efd35278ee6b77f03b4a77bf0f4fb1d&userid='+self.user+'&spoken=' + text_input)
        answer = sess.text
        answer = json.loads(answer)
        return answer['data']['info']['text']
    def TellRobot(self, text: str):
        '''
        告诉魔扣AI机器人你想对它说的话，它会对你进行回答
            Args:
                text:你想告诉机器人的话
            Returns:
                魔扣AI机器人对你的回答
                回答的话是文本(str)类型
            Raises:
                如果text参数的值不是str类型将会进行异常处理
        '''
        if type(text) == str:
            return self.SiZhi_Robot_think(text)
        return None
