#coding=utf-8  

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import datetime
import time
import json

from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler



define("port", default=9999, type=int)


class ChatHandler(WebSocketHandler):

    #建立websocket连接
    def open(self):

        self.sendFile = []
        self.file_list = []
        self.file_count = 0
        self.rootdir=''
        print("connection succeed")

        rootdir = os.getcwd()+'/analysis_recent_result'
        fileList = os.listdir(rootdir)
        fileList_mess = ''.join(str(e)+" " for e in fileList)
        fileList_mess = fileList_mess+'fileList'
        self.write_message(fileList_mess)

    #websocket接受信息
    def on_message(self, message):

        ##展示文件列表
        if(message[0:12]=='ask for fold'):
            file_list_mess =[]
            # print(message[13:])
            self.file_list=[]
            self.file_count=0
            self.rootdir = os.getcwd()+'/analysis_recent_result/'+message[13:]
            fileList = os.listdir(self.rootdir)
            for i in range(0,len(fileList)):
                filePath = os.path.join(self.rootdir,fileList[i])
                if os.path.isfile(filePath):
                    #如果不是Json文件直接跳过
                    if(filePath[len(filePath)-4:len(filePath)]!='json'):
                        pass
                    else:
                        self.file_list.append(filePath)
        
            file_list_mess = ''.join(str(e[-12:-5])+" " for e in self.file_list)
            file_list_mess = file_list_mess+'file'
            self.write_message(file_list_mess)

        ##展示单个json文件
        if(message[0:12]=='ask for json'):
            jsonFile = self.rootdir +'/'+ message[13:]+'.json'
            f=open(jsonFile)
            test = json.load(f)
            # print(test)
            self.write_message(test)
        
    #关闭websocket    
    def on_close(self):
        print('connection closed')
        pass

    #允许跨域请求
    def check_origin(self, origin):
        return True  

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/chat", ChatHandler),
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__), "template"),
        debug = True
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
