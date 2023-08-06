# -*- coding: utf-8 -*-
from ..base.Rule import Rule;
from ..base.RouterRequest import RouterRequest
from ..utils.RouteUtil import RouteUtil
import re

"""
 * 简易路由器规则类
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
class EasyRule(Rule):

    #参数匹配正则表达式
    PATHINFO_PARAMS_REGEX = r'<(\w+):?([^>]+)?>';

    PATHINFO_VARS_REGEX = r'<(\w+:?[^>]+)?>';

    #URL参数匹配正则表达式
    URL_PARAMS_REGEX = '<(\\w+)>';

    #参数左边分隔符
    PARAMS_LEFT_FLAG = "<";

    #参数左边分隔符
    PARAMS_RIGHT_FLAG = ">";

    REG_SPLIT = "/";

    def __init__(self,attrs = {}):

        super().__init__(attrs);
        self.patternParams = {}
        self.urlParams = {}
        self.urlTemplate = '';
        self.patternRegex = '';
        self.formatPatternParams()
        self.formatUrlParams()
        self.buildUrlRegex()
        self.buildPatternRegex()

        return ;

    def buildParamFlag(self,name):

        return  self.PARAMS_LEFT_FLAG + name + self.PARAMS_RIGHT_FLAG


    def formatPatternParams(self):

        regex = re.compile(self.PATHINFO_PARAMS_REGEX)
        matches = regex.findall(self.uri);
        if matches:
            for matche in matches:
                self.patternParams[matche[0]] = matche[1];

        return;

    def formatUrlParams(self):

        regex = re.compile(self.URL_PARAMS_REGEX)
        matches = regex.findall(self.action);
        if matches:
            for name in matches:
                self.urlParams[name] = self.buildParamFlag(name);

        return ;

    def buildUrlRegex(self):

        if not self.urlParams:
            self.urlRegex  = r'^' + self.action + '$';
            return

        replaceParams = {};
        for name in self.urlParams.keys():
            pattern = self.patternParams[name]
            replaceParams[self.buildParamFlag(name)] =  "(?P" + self.buildParamFlag(name) + pattern +")";

        self.urlRegex = r'^' + RouteUtil.replaceAll(self.action,replaceParams) +'$';

        return;

    def buildPatternRegex(self):

        replaceParams = {
            '.':'\\.',
            '*':'\\*',
            '$':'\\$',
        }

        for name in self.patternParams:
            key = self.PARAMS_LEFT_FLAG + name + self.PARAMS_RIGHT_FLAG
            pattern = self.patternParams[name]
            replaceParams[key] = "(?P" + self.buildParamFlag(name) + pattern + ")"

        regexParams = re.compile(self.PATHINFO_PARAMS_REGEX)
        matchesxParams  = regexParams.findall(self.uri)
        regexVars = re.compile(self.PATHINFO_VARS_REGEX)
        matchesVars = regexVars.findall(self.uri)

        urlTemplate = self.uri
        if matchesxParams:
            index = 0;
            for matche in matchesxParams:
                urlTemplate = urlTemplate.replace(self.buildParamFlag(matchesVars[index]),self.buildParamFlag(matche[0]))
                index = index + 1;
        else:
            urlTemplate = '';

        self.urlTemplate = urlTemplate;

        if not self.urlTemplate:
            self.patternRegex = r'^' + self.uri + '$';
            self.urlTemplate = self.uri;
        else:
            self.patternRegex = r'^' + RouteUtil.replaceAll(self.urlTemplate,replaceParams) + '$';

        return;


    # 解析请求路由
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def parseRequest(self,routerRequest:RouterRequest = None):

        pathinfo = routerRequest.getPathinfo();
        matches = re.match(self.patternRegex,pathinfo)
        if not matches:
            return False
        matcheParams = {}

        for name in self.patternParams:
            matcheParams[name] = matches.group(name)
        # 过滤参数,分离url 参数以及get 参数(多余的参数)
        uriReplaceParams = {}
        getParams = {}
        if matcheParams:
            urlParamsKeys = self.urlParams.keys()
            patternParamsKeys = self.patternParams.keys()
            for key in matcheParams:
                if key in urlParamsKeys:
                    uriReplaceParams[self.urlParams[key]] = matcheParams[key];
                elif key in patternParamsKeys:
                    getParams[key] =  matcheParams[key];

        if self.urlRegex:
            url = RouteUtil.replaceAll(self.action,uriReplaceParams)
        else:
            url = self.action

        # 过滤其他参数

        return [url,getParams]

    # 生成url地址
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def parseUrL(self, uri, params = {},routerRequest:RouterRequest = None):

        replaceParams = {}
        urlRegexParams = {}
        getParams = {};

        if uri is not self.urlRegex:
            matches = re.match(self.urlRegex,uri)
            if not matches:
                return False
            for key in self.urlParams:
                try:
                    urlRegexParams[key] = matches.group(key)
                except:
                    pass

        # 合并所有参数
        getParams.update(urlRegexParams)
        getParams.update(params)
        getParamskeys = getParams.keys();
        for key in self.patternParams:
            if key in getParamskeys:
                replaceParams[self.buildParamFlag(key)] = getParams[key]
                getParams.pop(key)
            else:
                replaceParams[self.buildParamFlag(key)] = ""
        replaceParams = RouteUtil.toStr(replaceParams)
        url = RouteUtil.replaceAll(self.urlTemplate,replaceParams);

        return [url,getParams]