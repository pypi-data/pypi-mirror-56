import requests,json,time

class Express:

    base_url = "https://biz.trace.ickd.cn"
    time = int(time.time())

    def __init__(self,url=None):
        self.base_url = url if url else "https://biz.trace.ickd.cn"
        self.time = int(time.time())
        
    def build_header(self):
        pass
    @classmethod
    def get_express(self,deliverynum):
        url = "{0}/auto/{1}?mailNo={1}&spellName=&exp-textName=&tk=705a7525&tm={2}".format(self.base_url,deliverynum,self.time)
        try:
            response = requests.get(url).text
            data = json.loads(response)
            if "status" in data and data["status"]:
                mailNo = data["mailNo"]
                expTextName = data["expTextName"]
                exp_data_list = data["data"]
                result = "快递公司:{0}\n快递单号:{1}\n".format(expTextName,mailNo)
                if len(exp_data_list)>0:
                    for i in exp_data_list[(len(exp_data_list)-1):]:
                        time = i["time"]
                        context = i["context"]
                        result+= time+"  "+context+ "\n"
                else:
                    result="您的快递可能还没有发货，请联系{0}".format(expTextName)
            else:
                result = "查询不到信息，请核对单号和快递公司是否正确"
        except Exception as err:
            print(err)
            result = "快递查询接口故障"
        return result
    
if __name__ == "__main__":
    s= Express.get_express("777005626187800")
    print(s)

