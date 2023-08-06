# -*- coding: utf-8 -*-
import importlib

"""
 * 路由器帮助类
 *<B>说明：</B>
 *<pre>
 *  提供基本类操作,获取属性值,设置属性等等
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
class RouteUtil:


    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def setAttrs(cls,object,attrDict = {}):

        for attr in attrDict:
            setattr(object, attr, attrDict[attr])


    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getModuleMeta(cls,clazz):

        if type(clazz) == str:
            packageClass = clazz.rsplit('.', 1)
            packageMeta = importlib.import_module(packageClass[0])
            return  getattr(packageMeta, packageClass[1])
        else:
            return clazz

    @classmethod
    def replaceAll(cls,str = '',replaceList = {}):

        newStr = '' + str
        for find in replaceList:
            replace = replaceList[find];
            newStr = newStr.replace(find,replace)

        return  newStr

    # 首字母大写
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def ucfirst(cls, str):

        return str[0].upper() + str[1:]

    @classmethod
    def toStr(cls,dataList = {}):

        data = {};
        for key in dataList:
            data[key] = str(dataList[key])

        return  data

