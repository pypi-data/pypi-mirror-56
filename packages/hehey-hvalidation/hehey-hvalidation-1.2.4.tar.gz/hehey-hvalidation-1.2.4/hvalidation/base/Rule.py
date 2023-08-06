# -*- coding: utf-8 -*-

from ..utils.ValidUtil import ValidUtil

"""
 * 验证规则
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
class Rule(object):

    # 默认场景
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    DEFUALT_SCENE = 'default';

    def __init__(self,ruleConf = []):

        # 验证的属性名
        # <B> 说明： </B>
        # <pre>
        # app 应用级别，forever 永远不失效
        # </pre>
        self.attrs = {};

        # 验证器列表
        # <B> 说明： </B>
        # <pre>
        # [
        #    ['boolean','skipOnEmpty'=>false]
        # ]
        # </pre>
        self.validators = []

        # 当验证错误是是否继续验证
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.goon = True;

        # 错误消息
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.message = '';

        # 场景
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.on = '';

        # 满足条件
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.when = None;

        attrConf = [];
        attrConf = attrConf + ruleConf
        attr = attrConf[0]
        attrList = [];
        if type(attr) is not list:
            attrList.append(attr)
        else:
            attrList = attr;

        self.attrs = attrList

        validator = attrConf[1]
        validatorList = [];
        if type(validator) is not list:
            validatorList.append(attr)
        else:
            validatorList = validator;

        self.validators = validatorList
        if len(attrConf) >= 3:
            attrs = attrConf[2]
            ValidUtil.setAttrs(self,attrs)


    def getMessage(self):

        return self.message

    def getValidators(self):

        return self.validators;

    def getGoon(self):

        return self.goon;

    def getAttrs(self):

        return self.attrs

    # 是否有效规则
    # <B> 说明： </B>
    # <pre>
    # 根据场景过滤出适合符合传入场景的rule
    # </pre>
    def isActive(self,scenes = [],attributes = {}):

        if self.on and (self.on != self.DEFUALT_SCENE or self.on not in scenes):
            return False

        if self.when and self.when(attributes) is False:
            return False;

        return True


