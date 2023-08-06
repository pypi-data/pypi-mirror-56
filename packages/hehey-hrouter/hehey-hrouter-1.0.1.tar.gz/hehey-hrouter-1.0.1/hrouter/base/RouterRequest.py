# -*- coding: utf-8 -*-

"""
 * 路由请求基类
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
class RouterRequest():

    def __init__(self,environ):

        self.url = '';
        self.params = {}
        self.environ = environ

        return ;

    def getPathinfo(self):

        path_info = self.environ['PATH_INFO'];

        return path_info.lstrip('/')

    def getMethod(self):

        return self.environ.get('REQUEST_METHOD','get').lower()

    def setRequestResult(self,result):

        if result:
            self.url = result[0];
            self.params = result[1]

        return ;

    def getRouteUrl(self):

        return self.url

    def getRouteParams(self):

        return self.params


"""
 * url路由web请求类
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
class WebRouterRequest(RouterRequest):

    def getPathinfo(self):

        path_info = self.environ['PATH_INFO'];

        return path_info.lstrip('/')


"""
 * url路由控制器台请求类
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
class ConsoleRouterRequest(RouterRequest):

    def getPathinfo(self):

        path_info = self.environ['PATH_INFO'];

        return path_info.lstrip('/')

