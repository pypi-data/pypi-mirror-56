# -*- coding: utf-8 -*-
import importlib
import time,datetime

"""
 * 类帮助类
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
class ValidUtil:

    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getAttrs(cls, object):

        attrs = object.__dict__;
        attrDict = {};
        for attr in attrs:
            if not attr.startswith("_"):
                attrDict[attr] = getattr(object, attr)

        return attrDict

    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getAttrValues(cls, object,attrNames = []):

        attrDict = {};
        for attrName in attrNames:
            attrDict[attrName] = getattr(object, attrName)

        return attrDict

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

        if isinstance(clazz,str):
            packageClass = clazz.rsplit('.', 1)
            packageMeta = importlib.import_module(packageClass[0])
            return  getattr(packageMeta, packageClass[1])
        else:
            return clazz

    @classmethod
    def replaceAll(cls, str='', replaceList={}):

        newStr = '' + str
        for find in replaceList:
            replace = replaceList[find];
            newStr = newStr.replace(find, replace)

        return newStr

    @classmethod
    def listToStr(cls, values = []):

        for i in range(0, values.__len__()):
            values[i] = str(values[i])

        return values

    # 字符串日期转时间戳
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def strtotime(self,strtime:str):

        datetimelist = strtime.split(' ')
        datelist = datetimelist[0].split('-');

        if len(datetimelist) >= 2:
            timelist =  datetimelist[1].split(":")
        else:
            timelist = [];

        dt_datetime_list = [0,0,0,0,0,0]

        for i in range(len(datelist)):
            dt_datetime_list[i] = int(datelist[i]);

        for i in range(len(timelist)):
            index = i + 3
            dt_datetime_list[index] = int(timelist[i]);

        year,month,day,hour, minute, second = dt_datetime_list;
        dtime = datetime.datetime(year,month,day,hour,minute,second)

        return int(time.mktime(dtime.timetuple()))

