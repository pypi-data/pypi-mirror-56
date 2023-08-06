# -*- coding: utf-8 -*-
from ..utils.ValidUtil import ValidUtil
from .ValidateResult import ValidateResult

"""
 * 验证器基类
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

class Validator(object):

    def __init__(self,attrs = {}):

        self.validation = None

        # 验证的数据
        # <B> 说明： </B>
        # <pre>
        # 或
        # </pre>
        self.attributes =  {};

        # 验证器名称
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.validatorName = ''

        # 验证错误提示信息
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.message = ''

        # 验证值为空时是否调用验证
        # <B> 说明： </B>
        # <pre>
        # true 表示　值为空时,不验证,false 表示值为空，继续验证
        # </pre>
        self.skipOnEmpty = True

        # 验证是否空方法
        # <B> 说明： </B>
        # <pre>
        # 一般函数或[$this,'isEmpty']
        # 比例利用php 的empty 函数验证空值
        # </pre>
        self.emptyFunc = None

        # 结果是否非
        # <B> 说明： </B>
        # <pre>
        # 如:!$result
        # </pre>
        self.non = False

        # 消息替换参数
        # <B> 说明： </B>
        # <pre>
        # 在验证validateValue中给设置params值
        #  {'min'=>'1','max'=>'10',..}
        # </pre>
        self.params = {}

        if attrs:
            ValidUtil.setAttrs(self,attrs)

    def setAttributes(self,attributes):

        self.attributes = attributes;

        return ;

    def getAttribute(self,attrName:str):

        attrNameList = attrName.split('.')
        attributeName = attrNameList.pop(0);
        if isinstance(self.attributes,dict):
            value = self.attributes[attributeName]
        else:
            value = getattr(self.attributes,attributeName)

        for attr in attrNameList:
            value = value.get(attr,None)

        return value;

    def setValidation(self,validation):

        self.validation = validation;

        return ;


    # 判断给定的值是否为空
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def isEmpty(self,value):

        if self.emptyFunc:
            return self.emptyFunc(value)
        else:
            if value:
                return False
            else:
                return True


    # 验证方法接口
    # <B> 说明： </B>
    # <pre>
    # 子类必须实现此方法
    # </pre>
    # param value 验证值
    # param name 验证名称
    def validateValue(self,value,name):

        return True

    # 验证规则
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # param rule
    def validateRule(self,rule):

        attrs = rule.getAttrs();
        validateResultList = [];
        for attrName in attrs:
            value = self.getAttribute(attrName)
            validateResultList.append(self.validate(value, attrName))

        if False in validateResultList:
            return ValidateResult(False, self.getMessage(), {})
        else:
            return ValidateResult(True)

    # 是否跳过验证
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # param values 属性值列表
    def isSkip(self,value):

        if self.skipOnEmpty and self.isEmpty(value):
            return True
        else:
            return False

    # 验证单值接口
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # param values 属性值列表
    # return boolean
    def validate(self,value,name = None):

        if self.isSkip(value):
            return True

        result = self.validateValue(value,name)
        if  self.non is True:
            result = bool(1-result)

        return result

    def getMessage(self):

        msg = self.message;
        if not msg:
            # 获取默认消息
            msg = self.validation.getDefaultMessage(self.validatorName);

        msg = self.formatMessage(msg,self.params)

        return msg;

    def formatMessage(self,message,params = {}):

        if not params:
            return message

        replaceList = {}
        paramsType = type(params)

        if paramsType is list:
            for index in range(len(params)):
                replaceList['{' + str(index) + '}'] = params[index]
        else:
            for key in params:
                replaceList['{' + key + "}"] = str(params[key])


        return ValidUtil.replaceAll(message,replaceList)

    def addParam(self,key,value):

        self.params[key] = value

        return ;

    def addParams(self,params = {}):

        self.params.update(params)

        return True
