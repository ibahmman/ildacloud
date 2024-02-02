import requests, json



class ParsianWeb():
    USER_ID = 42
    PASSWORD = 'kxsnb'
    TOKEN = "733422cd01b5bc0e184b605fc8166b072524885b4e64e9e6318a7992.50836432"


    def __init__(self, mobile) -> None:
        self.RECEIVER = mobile

    def send_code(self, *code):
        API_ADDRESS = 'https://api.parsianwebco.ir/webservice-send-sms/send'
        TEMPLATE_ID = 1
        MESSAGE_VARS = ','.join(code)
        data = {
            # 'cid': self.USER_ID,
            # 'cpass': self.PASSWORD,
            'token': self.TOKEN,
            'TemplateID': TEMPLATE_ID,
            'MessageVars': MESSAGE_VARS,
            'Receiver': self.RECEIVER,
            'delay': 1
        }
        headers = {
        "Content-Type": "application/x-www-form-urlencoded"
        }
        response = json.loads(requests.post(url=API_ADDRESS, data=data, headers=headers).content)
        # response = json.dumps(response, indent=4)
        return response
    
    def recovery_account(self, *message_vars):
        """
        message_vars
        __1__ = name and lastname
        __2__ = username
        __3__ = recovery link
        """

        API_ADDRESS = 'https://api.parsianwebco.ir/webservice-send-sms/send'
        TEMPLATE_ID = 2
        MESSAGE_VARS = ','.join(message_vars)
        data = {
            # 'cid': self.USER_ID,
            # 'cpass': self.PASSWORD,
            'token': self.TOKEN,
            'TemplateID': TEMPLATE_ID,
            'MessageVars': MESSAGE_VARS,
            'Receiver': self.RECEIVER
        }
        response = requests.post(url=API_ADDRESS, data=data)
        return response
    


# def test():
#     params = {
#         'token': "733422cd01b5bc0e184b605fc8166b072524885b4e64e9e6318a7992.50836432",
#         'TemplateID': 1,
#         'MessageVars': "Opz Test",
#         'Receiver': "09167332792",
#         'Delay': 1
#     }
#     headers = {
#     "Content-Type": "application/x-www-form-urlencoded"
#     }
#     r = requests.post('https://api.parsianwebco.ir/webservice-send-sms/send',
#     data=params, headers=headers)
#     response = json.loads(r.content)
#     result = json.dumps(response, indent=4)
#     print(result)