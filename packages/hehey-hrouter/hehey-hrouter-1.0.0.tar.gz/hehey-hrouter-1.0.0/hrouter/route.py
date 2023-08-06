# -*- coding: utf-8 -*-
from .base.RouterRequest import RouterRequest
from .base.BaseRouter import BaseRouter
from .utils.RouteUtil import RouteUtil
import inspect
import threading

# 注如露规则
# <B> 说明： </B>
# <pre>
# 以类名为key
# </pre>
def reg_route_rule(uri = '',**ruleConf):

    def decorator(func):

        currentModule = inspect.getmodule(func)
        if currentModule.__name__ == '__main__':
            actionUrl = func.__qualname__
        else:
            actionUrl = currentModule.__name__ + '.' + func.__name__

        action = ruleConf.pop('action',None)
        if action is not None:
            rule = {
                'uri': uri,
                'action': action,
            }
        else:
            rule = {
                'uri': uri,
                'action': actionUrl,
                'filter': True
            }

        rule.update(ruleConf)
        RouterManager.registerRule(rule)

        return func

    return decorator

"""
 * 路由管理器
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  router 组件基本配置
    router = RouterManager({
        'router':{
            #'clazz': 'hehe.core.hrouter.easy.EasyRouter.EasyRouter',# url 路由器,不填,则默认,一般不填
    
            #'routerRequest':'WebRouterRequest',# 路由规则
            # url 路由规则定义
            'rules':[
                #uri 请求地址规则,action 操作地址规则,method 请求方法,clazz 规则类,用于扩展
                #{'uri':'<news:\w+>/<id:\d+>','action':'<news>/index','method'='get','clazz'=>''},
                #{'uri':'<controller:\w+>/<action:\w+>','action':'<controller>/<action>'},
    
                {'uri':'<news:\w+>/<id:\d+>.html','action':'<news>/detail'}
            ],
    
            # action 规则配置
            'actionRule':{
                'filter': ['site', 'controllers', 'modules'],# 自动过滤包路径的关键词
                'suffix': ['Action', 'Controller'],# action 后缀 ['action 方法后缀','Controller 控制器类后缀']
                'func':'' # action 地址处理方法
            }
        }
    });
    
    
    # 注册路由规则-函数
    @reg_route_rule('user/getuserlist')
    def getuser(self):
    
        print("pass")
    
        return "<h1>您好</h1>"
    
    # 注册路由规则-类方法
    class NewsController:
    
        @reg_route_rule('news/list')
        def getindex(self):
    
            print("pass")
    
            return "<h1>您好</h1>"
    
        # 资讯详情
        def detail(self):
            print("pass")
    
            return "<h1>您好</h1>"
    
        pass
        
    # 运行路由
    routerRequest = router.runRoute({'PATH_INFO':"news/list"});
    # 获取解析后的路由地址
    routeUrl = routerRequest.getRouteUrl() # 获取路由解析后url地址,比如news/index
    routeParams = routerRequest.getRouteParams();# 获取路由的解析后参数{"id":1}
    # route = news/getindex
    print(routeUrl)
    
    # 生成地址
    url = router.buidlUrl('news/getindex',{"id":"10"})
    # url: news/list?id=10
    
    url = router.buidlUrl('getuser',{"id":"10"})
    # url: user/getuserlist?id=10
    
    url = router.buidlUrl('news/detail',{"id":"10"})
    
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
class RouterManager():

    # 路由规则
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    rules = []

    def __init__(self,**attrs):

        # 路由器配置
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.customRouter = {}

        # 当前路由器对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.urlRouter = None

        # 路由请求类型
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.routerRequest = 'WebRouterRequest';

        # 主线程路由对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.mainRouterRequest = '';

        self.threadLocal = threading.local()

        if attrs:
            RouteUtil.setAttrs(self,attrs)

    # 创建路由请求对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def makeRouterRequest(self,environ)->RouterRequest:

        routerRequestMeta = self.getRouterRequestMeta();

        return routerRequestMeta(environ)

    # 获取路由请求元
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getRouterRequestMeta(self):

        if isinstance(self.routerRequest,str):
            if self.routerRequest.find('.') == -1:
                routerRequestClazz = __package__ + '.base.RouterRequest.' +  self.routerRequest

            self.routerRequest = RouteUtil.getModuleMeta(routerRequestClazz)

        return self.routerRequest;

    # 获取路由请求对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getRouterRequest(self,routerRequest:RouterRequest):

        if routerRequest:
            return routerRequest;

        if hasattr(self.threadLocal, "routerRequest"):
            return self.threadLocal.routerRequest

        return self.mainRouterRequest;


    # 获取指定类型的Url路由对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getUrlRouter(self)->'BaseRouter':

        if self.urlRouter is None:
            routerConf = self.customRouter.copy();
            urlRouterClass = routerConf.get('clazz',None)
            if urlRouterClass is None:
                urlRouterClass = 'easy'
            else:
                routerConf.pop('clazz')

            if urlRouterClass.find('.') == -1:
                routerName = urlRouterClass;
                clazzName = RouteUtil.ucfirst(routerName) + 'Router'
                urlRouterClass = '{0}.{1}.{2}.{3}'.format(__package__,routerName,clazzName,clazzName)

            urlRouterMeta = RouteUtil.getModuleMeta(urlRouterClass)
            rules = routerConf.get('rules',[])
            routerConf['rules'] = rules + self.rules
            self.urlRouter = urlRouterMeta(routerConf)

        return self.urlRouter;



    # 运行路由器
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # param: environ 环境上下文参数
    def runRoute(self,environ)->'RouterRequest':

        routerRequest = self.makeRouterRequest(environ);
        self.parseRequest(routerRequest);
        self.mainRouterRequest = routerRequest;
        self.threadLocal.routerRequest = routerRequest;

        return routerRequest

    # 解析请求地址
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def parseRequest(self,routerRequest:RouterRequest):

        self.getUrlRouter().parseRequest(routerRequest)

        return routerRequest

    # 构建url 地址
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param uri 路由url地址
    # :param vars 参数
    # :param options 其他配置
    def buildUrl(self,uri = '',vars = {},routerRequest:RouterRequest = None,**options):

        routerRequest = self.getRouterRequest(routerRequest);

        return self.getUrlRouter().buildUrL(uri,vars,routerRequest,**options)

    # 注册路由规则
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param rule 路由规则
    @classmethod
    def registerRule(cls,rule = {}):

        cls.rules.append(rule)

        return ;


