import tkinter
import ExpressInfo
from tkinter import *
# import time
# import urllib.parse
main_window = tkinter.Tk()  # GUI界面初始化
main_window.title('基于图像识别的快递物流信息跟踪系统')
main_window.iconbitmap('py.ico')
main_window.geometry('600x400')
menubar = tkinter.Menu(main_window)  # 设置菜单栏Exit选项
main_menu = tkinter.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Menu', menu=main_menu)
main_menu.add_command(label='Exit', command=main_window.quit)
main_window.config(menu=menubar)
iscrollbar = Scrollbar(main_window)  # 设置UP滚动条
iscrollbar.place(x=575, y=0, anchor='nw')
iscrollbar.pack(side=RIGHT, ipady=80, anchor='ne')
infolist = Listbox(main_window, yscrollcommand=iscrollbar.set, width=45, height=12)  # 设置UP ListBox
infolist.place(x=255, y=0, anchor='nw')
iscrollbar.config(command=infolist.yview)  # 关联UP滚动条与ListBox
sscrollbar = Scrollbar(main_window)  # 设置DOWN滚动条
sscrollbar.pack(side=RIGHT, ipady=55, anchor='se')
shippinglist = Listbox(main_window, yscrollcommand=sscrollbar.set, width=81, height=9)  # 设置DOWN ListBox
shippinglist.place(x=0, y=230, anchor='nw')
sscrollbar.config(command=shippinglist.yview)  # 关联DOWN滚动条与ListBox
expressinfo = ExpressInfo.ExpressInfo(infolist, shippinglist)  # 实例化ExpressInfo类
upload_button = tkinter.Button(main_window, text='选择图片', font=("宋体", 10, 'bold'), width=10, height=1, command=expressinfo.openfile)  # 设置选择图片按钮并关联相应函数
req_button = tkinter.Button(main_window, text='查询信息', font=("宋体", 10, 'bold'), width=10, height=1, command=expressinfo.req_ocr)  # 设置查询信息按钮并关联相应函数
upload_button.place(x=0, y=205, anchor='nw')
req_button.place(x=160, y=205, anchor='nw')
main_window.mainloop()

