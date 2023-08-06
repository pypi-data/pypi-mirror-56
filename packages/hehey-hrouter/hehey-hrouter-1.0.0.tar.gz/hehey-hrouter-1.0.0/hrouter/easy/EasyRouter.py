# -*- coding: utf-8 -*-

from ..base.RouterRequest import RouterRequest
from ..base.BaseRouter import BaseRouter
from .EasyRule import EasyRule
from urllib.parse import urlencode


"""
 * 简易路由器
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
class EasyRouter(BaseRouter):

    def __init__(self,attrs = {}):

        super().__init__(attrs)
        self.ruleClass = EasyRule
        self.addRules(self.rules)

        return ;

    # 生成url地址
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def buildUrL(self,uri = '',params = {},routerRequest:RouterRequest = None,**options):

        method = routerRequest.getMethod()
        rules = self.getRules(method)
        result = self.executeUrlRules(uri,params,rules,routerRequest)

        url = '';
        if not result:
            url = uri
        else:
            url = result[0]
            params = result[1];

        # 构建出最终的url 地址
        if params:
            url = url + '?' + urlencode(params)

        return url;


    # 生成url地址
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def parseRequest(self, routerRequest):

        method = routerRequest.getMethod()
        rules = self.getRules(method)
        result = self.executeRequestRules(routerRequest, rules)
        routerRequest.setRequestResult(result);

        return routerRequest
