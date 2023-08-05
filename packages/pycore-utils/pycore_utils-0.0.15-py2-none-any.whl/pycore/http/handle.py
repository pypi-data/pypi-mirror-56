# coding=utf-8
from pycore.http import ErrorCode
from pycore.utils.logger_utils import LoggerUtils
from pycore.utils.stringutils import StringUtils

logger = LoggerUtils('access').logger


class HttpRequest(object):

    def __init__(self, addr):
        self.method = None
        self.url = None
        self.protocol = None
        self.head = dict()
        self.request_data = dict()
        self.response_line = ErrorCode.NOT_FOUND
        self.response_head = dict()
        self.response_body = 'No Something To Do'
        self.session = None
        self.addr = addr

    def log_message(self, formatstr, *args):
        logger.info("%s:%d - - %s\n" % (self.addr[0], self.addr[1], formatstr % args))

    def passRequestLine(self, request_line):
        header_list = request_line.split(' ')
        self.log_message(request_line)
        self.method = header_list[0].upper()
        self.url = header_list[1]
        self.protocol = header_list[2]

    def passRequestHead(self, request_head):
        head_options = request_head.split('\r\n')
        for option in head_options:
            key, val = option.split(': ', 1)
            self.head[key] = val

    def passRequestData(self, body):
        if self.method == 'POST':
            self.request_data = {}
            request_body = body.split('\r\n\r\n', 1)[1]
            self.log_message("param:%s", str(request_body))
            parameters = request_body.split('&')  # 每一行是一个字段
            for i in parameters:
                if i == '':
                    continue
                key, val = i.split('=', 1)
                self.request_data[key] = val
        if self.method == 'GET':
            if self.url.find('?') != -1:  # 含有参数的get
                self.request_data = {}
                req = self.url.split('?', 1)[1]
                s_url = self.url.split('?', 1)[0]
                self.log_message("param:%s", str(req))
                parameters = req.split('&')
                for i in parameters:
                    key, val = i.split('=', 1)
                    self.request_data[key] = val
                self.url = s_url

    def passRequest(self, request):
        request = request.decode('utf-8')
        if len(request.split('\r\n', 1)) != 2:
            return
        request_line, body = request.split('\r\n', 1)
        request_head = body.split('\r\n\r\n', 1)[0]  # 头部信息
        self.passRequestLine(request_line)
        self.passRequestHead(request_head)
        self.passRequestData(body)
        self.do()

    def do(self):
        pass

    def getResponse(self):
        response = self.response_line + StringUtils.dict2str(self.response_head) + '\r\n' + self.response_body
        self.log_message("return:%s", str(response))
        return response
