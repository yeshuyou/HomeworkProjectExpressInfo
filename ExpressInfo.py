import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import json
import base64
# import time
# import urllib.parse


class ExpressInfo:
    image_data = ''  # 原始图片数据初始化
    data_receive = {}  # 最终物流数据初始化
    infolist = []  # GUI ListBox UP
    shippinglist = [] # GUI ListBox DOWN

    def __init__(self,infolist,shippinglist):
        self.infolist = infolist
        self.shippinglist = shippinglist
        return

    def find_com(self,data_receive):  # 将百度云识别图片文字API返回数据与本地存储（预先从聚合数据API获取）的物流公司名编号对应表比对，获取公司编号
        with open("com_no.txt", mode='r') as f:
            no_data = f.read()
        data_com_no = json.loads(no_data)
        # print("data_com_no['result']:", data_com_no['result'])
        # for i in data_com_no['result']:
        #     print("com:%s no:%s" % (i['com'], i['no']))
        for i in data_com_no['result']:
            for j in data_receive['words_result']:
                if i['com'] in j['words']:
                    return i['no']
        return 'null'

    def find_num(self,data_receive):  # 从百度云识别图片文字API返回数据获取运单号码
        for i in data_receive['words_result']:
            if i['words'].isdigit():
                return i['words']
        return 'null'

    def req_token(self):  # 请求百度云API请求参数Access_Token
        req = requests.get(
            'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=4TF30EIsQMEIMy5V5QMb27xd&client_secret=wdOcRyzi1bCNWFyT8u3IGGsGVHtIXWyn')
        data_token = json.loads(req.text)
        # print("data_token['access_token']:", data_token['access_token'])
        return data_token

    def req_shippinginfo(self,data_receive):  # 使用获取到的快递公司编号及运单号码请求聚合数据常用快递API以获取物流信息
        no = self.find_com(data_receive)
        if no == 'null':
            tkinter.messagebox.showerror(title='识别失败', message='未能识别快递公司或运单号码')
            self.infolist.delete(0, END)
            return
        num = self.find_num(data_receive)
        if no == 'null':
            tkinter.messagebox.showerror(title='识别失败', message='未能识别快递公司或运单号码')
            self.infolist.delete(0, END)
            return
        # print(find_com(data_receive))
        # print(find_num(data_receive))
        req = requests.get('http://v.juhe.cn/exp/index?key=941ebdddef178abc2c40f0db1d761de3&com=' + no + '&no=' + num)
        sdata_receive = json.loads(req.text)
        for i in sdata_receive['result']['list']:
            self.shippinglist.insert(END, i['datetime'])
            self.shippinglist.insert(END, i['remark'])
            self.shippinglist.insert(END, i['zone'])
        tkinter.messagebox.showinfo(title='查询成功', message='查询成功')

    def req_ocr(self):  # 使用选择图片请求百度云图片文字识别API以获取图片文字信息
        base64_data = base64.b64encode(self.image_data)
        # ur = urllib.parse.quote(base64_data)
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + self.req_token()['access_token']
        # url = 'https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request?access_token='+data_token['access_token']
        # url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/receipt?access_token='+data_token['access_token']
        data = {'image': base64_data}
        headers = {'Content-Type': 'multipart/form-data'}
        req = requests.post(url, headers=headers, data=data)
        print(req.text)
        data_receive = json.loads(req.text)
        print("data_receive['words_result']:", data_receive['words_result'])
        # for i in data_receive['words_result']:
        #     print("words:%s" % (i['words']))
        for i in data_receive['words_result']:
            self.infolist.insert(END, i['words'])
        self.req_shippinginfo(data_receive)
        return data_receive
        # ret_code = 1
        # while ret_code !=3:
        #     url = 'https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/get_request_result?access_token='+data_token['access_token']
        #     data = {'request_id': data_receive['result'][0]['request_id'], 'result_type': 'json'}
        #     headers = {'Content-Type': 'multipart/form-data'}
        #     req = requests.post(url, headers=headers, data=data)
        #     print(req.text)
        #     request_receive = json.loads(req.text)
        #     ret_code = request_receive['result']['ret_code']
        #     time.sleep(3)
        # print("request_receive['result']['result_data']:", request_receive['result']['result_data'])

    def openfile(self):  # 选择识别图片并显示至窗口
        fname = tkinter.filedialog.askopenfilename(title='选择图片', filetypes=[('All Files', '*')])
        with open(fname, 'rb') as f:
            self.image_data = f.read()
        load = Image.open(fname)
        load = load.resize((250, 200))
        render = ImageTk.PhotoImage(load)
        img = Label(image=render, width=250, height=200)
        img.image = render
        img.place(x=0, y=0)

