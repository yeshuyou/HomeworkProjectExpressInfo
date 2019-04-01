程序名称：基于图像识别的快递物流信息跟踪系统
程序功能：智能识别快递运单照片上的快递公司及运单号码，并自动追踪物流信息显示至屏幕。
使用说明：点击选择图片按钮选择要查询的快递单据照片，点击查询信息进行一键查询。图片文字识别信息显示于右上方滚动框内，实时快递物流跟踪信息显示于下方滚动框内。若未能从图片中识别出快递单据则弹出错误信息并清空滚动框，若查询成功则弹出提示信息。
调用API：百度云通用文字识别（高精度版）、聚合数据常用快递。
代码阐释：
MainWindow.py程序入口，在其中实现GUI初始化，并实例化ExpressInfo类以实现功能。
ExpressInfo.py定义类ExpressInfo。
类
ExpressInfo
成员变量
    image_data  # 原始图片数据初始化
    data_receive  # 最终物流数据初始化
    infolist  # GUI ListBox UP
    shippinglist # GUI ListBox DOWN
成员函数
    find_com(self,data_receive)  # 将百度云识别图片文字API返回数据与本地存储（预先从聚合数据API获取）的物流公司名编号对应表比对，获取公司编号
    find_num(self,data_receive)  # 从百度云识别图片文字API返回数据获取运单号码
    req_token(self)  # 请求百度云API请求参数Access_Token
    req_shippinginfo(self,data_receive)  # 使用获取到的快递公司编号及运单号码请求聚合数据常用快递API以获取物流信息
    req_ocr(self)  # 使用选择图片请求百度云图片文字识别API以获取图片文字信息
    openfile(self)  # 选择识别图片并显示至窗口
心得体会：调试代码是相当枯燥并且苦恼的过程，特别是语法学得不扎实的时候，相当多的问题都需要一边百度一边处理，整个过程花了12个小时左右，遇到一个大坑浪费了很久的时间。百度云API技术文档说明通过Post提交请求，Body参数Image需要将图片进行base64编码后进行urlencode，Header参数Content-Type值为application/x-www-form-urlencoded，请求之后返回错误信息"error_code":216201,"error_msg":"image format error"。更换图片及图片大小格式后仍然报错，在百度上查询大部分人是因为转码后前面添加了一串字符data:image/jpg;base64，但是我的情况不是这样，并且我进行base64编码后进行urlencode后可以解码回原始数据，写为图片后也正常显示，折腾了几个小时无果，后面终于发现一篇介绍百度OCR文字识别接口的博文的末尾提到了这个坑。进行base64编码后不需要再进行urlencode，同时Header参数Content-Type值应为multipart/form-data，死马当活马医地试了一下问题才解决了。