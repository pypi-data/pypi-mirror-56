# -*- coding: utf-8 -*-
from .RouterRequest import RouterRequest
from ..utils.RouteUtil import RouteUtil

"""
 * url 路由器基类
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
class BaseRouter():

    GET_RULE_METHOD = 'get';
    POST_RULE_METHOD = 'post';
    PUT_RULE_METHOD = 'put';
    DELETE_RULE_METHOD = 'delete';
    ANY_RULE_METHOD = 'any';
    MAP_RULE_METHOD = 'map';
    DOMAIN_RULE_METHOD = 'domain';

    def __init__(self,attrs = {}):

        # 规则队列列表
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.ruleList = {}

        # 地址中是否添加后缀,比如.html
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.suffix = False

        # 路由规则定义列表
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.rules = []

        # 路由规则类
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.ruleClass = '';

        # action 规则
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.actionRule = {
            # 'filter':['sites','controllers','modules'],
            # 'suffix':['Action','Controller'],
            # 'func':None
        }

        # 初始化
        if attrs :
            RouteUtil.setAttrs(self,attrs)


    # 添加路由规则
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def addRules(self,rules = [],method = ''):

        routerRuleList = self.buildRules(rules)
        if method:
            if method in self.ruleList.keys():
                self.ruleList[method] = self.ruleList[method] + routerRuleList
            else:
                self.ruleList[method] = routerRuleList
        else:
            for routerRule in routerRuleList:
                method = routerRule.getMethod()
                if method not in self.ruleList.keys():
                    self.ruleList[method] = []

                self.ruleList[method].append(routerRule)

        return;

    # 生成路由规则对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def buildRule(self,ruleConf = {}):

        ruleClass = ruleConf.get('clazz',self.ruleClass)
        filter = ruleConf.pop('filter',None)
        if filter is not None:
            ruleConf['action'] = self.formatActionUrl(ruleConf['action'])

        ruleClasssMeta = RouteUtil.getModuleMeta(ruleClass)
        rule = ruleClasssMeta(ruleConf)

        return rule


    # 批量生成路由规则对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def buildRules(self,rules = []):

        ruleList = [];
        for rule in rules:
            ruleList.append(self.buildRule(rule))

        return ruleList;

    # 获取指定方法的路由对象列表
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getRules(self,method):

        rules = self.ruleList.get(method,None)
        if rules:
            return rules

        if method in self.ruleList.keys():
            self.ruleList[method] = self.buildRules(self.ruleList[method])
            return self.ruleList[method];

        return []

    # 执行路由解析规则
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def executeRequestRules(self,routerRequest:RouterRequest,rules = []):

        if not rules:
            return False

        result = False;
        for rule in rules:
            result = rule.parseRequest(routerRequest)
            if result:
                break

        return result

    # 执行路由url构建规则
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def executeUrlRules(self,url = '',vars = {}, rules = [], routerRequest:RouterRequest = None):

        if not rules:
            return False
        result = False
        for rule in rules:
            result = rule.parseUrL(url,vars,routerRequest)
            if result:
                break

        return result

    # 生成url地址
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def buildUrL(self,url = '',vars = {},routerRequest:RouterRequest = None,**options):

        pass

    # 生成url地址
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def parseRequest(self, routerRequest:RouterRequest):

        pass

    # 格式化路由地址
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def formatActionUrl(self, action:str)->str:

        # 自定义处理方法
        func = self.actionRule.get('func', None);
        if func:
            funcMeta = RouteUtil.getModuleMeta(func)
            return funcMeta(action)

        actionpos = action.find('.');
        if actionpos == -1:
            return action;

        filterList = self.actionRule.get('filter',None);
        if filterList is not None:
            for filter in filterList:
                action = action.replace(filter + '.','')

        actions = action.split('.')
        actions.reverse()
        actionsCount = len(actions) - 1

        suffixList = self.actionRule.get('suffix', None);
        if suffixList:
            for index in range(len(suffixList)):
                suffix = suffixList[index]
                if (index <= actionsCount):
                    actionName = actions[index]
                    actionName = actionName[0].lower() + actionName[1:]
                    actions[index] = actionName.replace(suffix,'')

        actions.reverse()

        return '/'.join(actions)
