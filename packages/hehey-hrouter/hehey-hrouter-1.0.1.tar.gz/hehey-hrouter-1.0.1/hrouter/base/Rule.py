# -*- coding: utf-8 -*-
from .RouterRequest import RouterRequest
from ..utils.RouteUtil import RouteUtil

"""
 * url 规则类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  略
 *</pre>
 *<B>日志：</B>
 *<pre>
 *  略
 *</pre>
 *<B>注意事项：</B>
 *<pre>
 *  略
 *</pre>
"""
class Rule():

    URL_RULE_NAME = 'urlRule';
    PATTERN_NAME = 'pattern';

    def __init__(self,attrs = {}):

        #  pathinfo 正则表达式
        # <B> 说明： </B>
        # <pre>
        # 基本格式:^(?<controller>\w+)/(?<action>\w+)$
        # </pre>
        self.uri = ''

        #  url 正则表达式
        # <B> 说明： </B>
        # <pre>
        # 用于匹配url 的正则表达式
        # 本格式:^(?<controller>\w+)/(?<action>\w+)$
        # </pre>
        self.urlRegex = '';

        #  验证pathinfo 地址的正则表达式
        # <B> 说明： </B>
        # <pre>
        # 　略
        # </pre>
        self.patternRegex = '';

        #  url 规则
        # <B> 说明： </B>
        # <pre>
        # 基本格式:<controller>/<action>
        # 比如:
        # pathinfoRule:<controller:\w+>/<id:\d+>
        # url 地址可以使用controller,id 参数
        # url 最终格式可以有:
        # post/<id>
        # <controller>/<id>
        # </pre>
        self.action = '';

        #  验证范围方法
        # <B> 说明： </B>
        # <pre>
        # 　略
        # </pre>
        self.method = 'get';

        if attrs:
            RouteUtil.setAttrs(self,attrs)

        return ;


    def getMethod(self):

        return self.method

    # 生成url地址
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def parseUrL(self,url,params = {},routerRequest = RouterRequest):

        pass

    # 解析请求路由
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def parseRequest(self,routerRequest = RouterRequest):

        pass;