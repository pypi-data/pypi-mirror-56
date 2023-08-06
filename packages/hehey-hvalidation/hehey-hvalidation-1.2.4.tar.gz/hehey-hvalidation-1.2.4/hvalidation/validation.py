# -*- coding: utf-8 -*-

from .base.Rule import Rule
from .utils.ValidUtil import ValidUtil
from .base.ValidateResult import ValidateResult
from .validator.FuncValidator import FuncValidator
from .base.Validator import Validator
import types
from inspect import isfunction
import inspect

"""
 * 验证器管理类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 * validateData = {
 *    'name':'admin',
 *    'userid':10,
 *    'age':20
 * };
 * validateRules = [
 *     ['name',[['minlen',{'min':10,'max':20}]],{'message':'请输入一个10-20位的字符串'}],
 *     ['userid',[['!empty']],{'message':'user_id 不能为空'}],
 *     ['age',[['number']],{'message':'请输入0-9的数字'}],
 * ];
 *
 * validation = Validation();
 * validateResult = validation.validate(validateData,validateRules);
 * if validateResult == false:
 *     validation.getFirstError();
 * e.g 验证多个属性
 * [['userid','name'],[['!empty']],{'message':'参数不能为空'}],
 * 
 * e.g 定义多个验证类型，支持与或
 * ['name',[['!empty'],['minlen',{'min':10,'max':20}]],{'message':'请输入一个10-20位的字符串'}]
 * ['name',['or',['boolean'],['minlen',{'min':10,'max':20}]],{'message':'请输入一个10-20位的字符串或布尔型'}],
 *
 * e.g 新增验证类型
 * validation = Validation();
 * validation.addValidator('customType','hehe.core.validate.BooleanValidate','自定义消息内容');
 *
 * e.g 直接实例化验证类，调用验证类方法
 * validation = Validation();
 * validateResult = validation.callValidator('range',20,{'min':10,'max':20});
 *
 * e.g 快捷方式验证-直接调用验证器方法
 * validation = Validation();
 * validateResult = validation.eq('12',number=12]);
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

# 注册验证器
def reg_validator(message = '',alias = ''):

    def decorator(validator):
        name = alias;
        if not name:
            name = validator.__name__
        Validation.registerValidator(name, validator,message)

        return validator

    return decorator


# 注册类属性的验证规则
def reg_valid_rule(validator,**ruleConf):

    def decorator(property):
        clazzModule = inspect.getmodule(property).__name__
        clazz = clazzModule + '.' + property.__qualname__.split('.')[0];
        propertyName = property.__name__;
        validatorAttr = {}
        if ruleConf:
            propertyName = ruleConf.get('property',propertyName);
            validatorAttr = ruleConf.get('attrs', {});

        Validation.registerValidRule(clazz, propertyName,[validator,validatorAttr])

        return property

    return decorator

class Validation(object):

    # 验证器定义
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    validators = {
        'required':{'clazz':'RequiredValidator.RequiredValidator','message':'必须字段'},
        'empty': {'clazz': 'EmptyValidator.EmptyValidator', 'message': '输入的值必须为空'},
        'float': {'clazz': 'FloatValidator.FloatValidator', 'message': '请输入合法的浮点数'},
        'int': {'clazz': 'IntValidator.IntValidator', 'message': '请输入合法的整型数'},
        'boolean': {'clazz': 'BooleanValidator.BooleanValidator', 'message': '你输入的值非布尔值类型'},
        'tel': {'clazz': 'TelValidator.TelValidator', 'message': '你输入的手机号格式错误'},
        'date': {'clazz': 'DateValidator.DateValidator', 'message': '你输入的日期格式错误,正确日期格式为:{format}'},
        'rangedate': {'clazz': 'RangeDateValidator.RangeDateValidator', 'message': '你输入的日期范围有误!'},
        'email': {'clazz': 'EmailValidator.EmailValidator', 'message': '你输入的邮箱格式错误！'},
        'ip': {'clazz': 'IpValidator.IpValidator', 'message': '你的输入ip 格式有误！'},
        'ip4': {'clazz': 'IpValidator.IpValidator','mode':"ip4", 'message': '你的输入ip 格式有误！'},
        'ip6': {'clazz': 'IpValidator.IpValidator','mode':"ip6", 'message': '你的输入ip 格式有误！'},
        'url': {'clazz': 'UrlValidator.UrlValidator', 'message': '请输入一个合法的网络地址！'},
        'range': {'clazz': 'RangeValidator.RangeValidator', 'message': '请输入一个合法的{min}-{max}数值！'},
        'compare': {'clazz': 'CompareValidator.CompareValidator', 'message': '请输入合法的值！'},
        'eq': {'clazz': 'EqualValidator.EqualValidator', 'message': '请输入一个等于{number}的值'},
        'gt': {'clazz': 'CompareValidator.CompareValidator','operator':'gt','message': '请输入一个大于{number} 的数值！'},
        'egt': {'clazz': 'CompareValidator.CompareValidator', 'operator': 'egt', 'message': '请输入一个大于等于 {number} 的数值！'},
        'lt': {'clazz': 'CompareValidator.CompareValidator', 'operator': 'lt', 'message': '请输入一个小于 {number} 的数值！'},
        'elt': {'clazz': 'CompareValidator.CompareValidator', 'operator': 'elt', 'message': '请输入一个小于等于{number} 的数值！'},
        'minlen': {'clazz': 'LengthValidator.LengthValidator', 'operator': 'egt', 'message': '请输入一个长度最少是 {number} 的字符串！'},
        'maxlen': {'clazz': 'LengthValidator.LengthValidator', 'operator': 'elt', 'message': '请输入一个长度最多是 {number} 的字符串！'},
        'len': {'clazz': 'RangeLengthValidator.RangeLengthValidator', 'message': '请输入一个长度介于 {min} 和 {max} 之间的字符串！'},
        'currency': {'clazz': 'CurrencyValidator.CurrencyValidator', 'message': '请输入一个保留{{point}}位小数的货币数值！'},
        'ch': {'clazz': 'ChineseValidator.ChineseValidator', 'message': '请输入字符必须为中文！'},
        'en': {'clazz': 'EnglishValidator.EnglishValidator', 'message': '请输入字符必须为英文！'},

        'alpha': {'clazz': 'CharValidator.CharValidator','mode':"alpha", 'message': '请输入的字符必须包含字母字符！'},
        'alphaNum': {'clazz': 'CharValidator.CharValidator', 'mode': "alphaNum", 'message': '请输入的字符必须包含字母、数字！'},
        'alphaDash': {'clazz': 'CharValidator.CharValidator', 'mode': "alphaDash", 'message': '请输入的字符包含字母、数字、破折号（ - ）以及下划线（ _ ）！'},

        'inlist': {'clazz': 'InValidator.InValidator', 'message': '输入的值必须为{numbers}！'},
        'vlist': {'clazz': 'ListValidator.ListValidator', 'message': '你列表的值类型格式错误！'},
        'enum': {'clazz': 'InValidator.InValidator', 'message': '输入的值必须为{numbers}！'},
        'notin': {'clazz': 'InValidator.InValidator','non':True, 'message': '输入的值必须为{numbers}！'},

        'eqstrfield': {'clazz': 'CompareFieldValidator.CompareFieldValidator', 'comparetype': "str", 'operator': 'eq','message': '输入的{field1}与{field2}的值必须相等'},

        'eqintfield': {'clazz': 'CompareFieldValidator.CompareFieldValidator','comparetype':"int", 'operator': 'eq','message': '输入的{field1}与{field2}的值必须相等'},
        'gtintfield': {'clazz': 'CompareFieldValidator.CompareFieldValidator', 'comparetype':"int",'operator': 'gt', 'message': '请输入{field2} 的值必须大于{field1}！'},
        'egtintfield': {'clazz': 'CompareFieldValidator.CompareFieldValidator','comparetype':"int", 'operator': 'egt', 'message': '请输入{field2} 的值必须大于等于{field1}！'},
        'ltintfield': {'clazz': 'CompareFieldValidator.CompareFieldValidator', 'comparetype':"int",'operator': 'lt', 'message': '请输入{field2} 的值必须小于{field1}！'},
        'eltintfield': {'clazz': 'CompareFieldValidator.CompareFieldValidator','comparetype':"int",'operator': 'elt', 'message': '请输入{field2} 的值必须小于等于{field1}！'},

        'eqdatefield': {'clazz': 'CompareFieldValidator.CompareFieldValidator', 'comparetype': "date", 'operator': 'eq','message': '输入的{field1}与{field2}的值必须相等'},
        'gtdatefield': {'clazz': 'CompareFieldValidator.CompareFieldValidator', 'comparetype': "date", 'operator': 'gt','message': '请输入{field2} 的值必须大于{field1}！'},
        'egtdatefield': {'clazz': 'CompareFieldValidator.CompareFieldValidator', 'comparetype': "date", 'operator': 'egt','message': '请输入{field2} 的值必须大于等于{field1}！'},
        'ltdatefield': {'clazz': 'CompareFieldValidator.CompareFieldValidator', 'comparetype': "date", 'operator': 'lt','message': '请输入{field2} 的值必须小于{field1}！'},
        'eltdatefield': {'clazz': 'CompareFieldValidator.CompareFieldValidator', 'comparetype': "date", 'operator': 'elt','message': '请输入{field2} 的值必须小于等于{field1}！'},

    }

    # 验证类规则
    # <B> 说明： </B>
    # <pre>
    # 以类名为key
    # </pre>
    rules = {}

    def __init__(self):

        # 验证错误消息
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.errors = []

        self.validators = self.__class__.validators.copy();
        self.rules = self.__class__.rules.copy();

        # 注册验证器的快捷方式
        self.registerShortcutValidator()

        return ;

    # 快捷方法定义 start,用于ide
    def required(self,value,*attrs,**kwattrs):
        pass

    def empty(self,value,*attrs,**kwattrs):
        pass

    def boolean(self,value,*attrs,**kwattrs):
        pass

    def tel(self,value,*attrs,**kwattrs):
        pass

    def date(self,value,*attrs,**kwattrs):
        pass

    def email(self,value,*attrs,**kwattrs):
        pass

    def ip(self,value,*attrs,**kwattrs):
        pass

    def url(self,value,*attrs,**kwattrs):
        pass

    def range(self,value,*attrs,**kwattrs):
        pass

    def eq(self,value,*attrs,**kwattrs):
        pass

    def compare(self,value,*attrs,**kwattrs):
        pass

    def float(self,value,*attrs,**kwattrs):
        pass

    def gt(self,value,*attrs,**kwattrs):
        pass

    def egt(self,value,*attrs,**kwattrs):
        pass

    def lt(self,value,*attrs,**kwattrs):
        pass

    def elt(self,value,*attrs,**kwattrs):
        pass

    def minlen(self,value,*attrs,**kwattrs):
        pass

    def maxlen(self,value,*attrs,**kwattrs):
        pass

    def len(self,value,*attrs,**kwattrs):
        pass

    def currency(self,value,*attrs,**kwattrs):
        pass

    def ch(self,value,*attrs,**kwattrs):
        pass

    def en(self,value,*attrs,**kwattrs):
        pass

    def inlist(self,value,*attrs,**kwattrs):
        pass

    # 注册模板过滤器
    # <B> 说明： </B>
    # <pre>
    # 对外唯一入口
    # </pre>
    @classmethod
    def registerValidator(cls, alias, validator,message):

        cls.validators[alias] = {'clazz':validator,'message':message}

        return ;

    # 注册验证规则
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def registerValidRule(cls, clazz,attrName, rule = []):

        clazzRule = cls.rules.get(clazz,None)
        if clazzRule is None:
            clazzRule = {};
            clazzRule[attrName] = [rule]
        else:
            clazzRule[attrName].append(rule)

        cls.rules[clazz] = clazzRule;

        return;

    # 注册验证规则
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getValidRule(cls, clazz):

        clazzRule = cls.rules.get(clazz, {})
        if not clazzRule:
            return None;

        ruleList = []

        for attrName,rules in clazzRule.items():
            ruleList.append([attrName,rules])

        return ruleList

    # 获取所有错误消息
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def clearErrors(self):

        self.errors = [];

        return;

    # 获取第一个错误消息
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getFirstError(self):

        if self.errors:
            return self.errors[0];
        else:
            return '';

    # 添加错误消息
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def addError(self,message = ''):

        self.errors.append(message)

        return;

    # 获取所有错误消息
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getErrors(self):

        return self.errors

    # 是否错误消息
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def hasError(self):

        if self.errors.count() > 0:
            return True
        else:
            return False

    # 验证值
    # <B> 说明： </B>
    # <pre>
    # 验证入口,支持验证dict,object
    # </pre>
    # param rules 验证规则
    # param attributes 验证值列表
    # param scenes 场景列表
    # param clearErrors 是否清除上次验证结果
    #
    def validate(self,attributes = {},rules = [],scenes = [],clearErrors = True):
        # 获取类规则
        if not isinstance(attributes, dict):
            object = attributes;
            attributes = ValidUtil.getAttrs(attributes)
            # 读取类的规则
            if not rules:
                clazzModule = inspect.getmodule(object.__class__).__name__;
                clazz = clazzModule + '.' + object.__class__.__name__
                clazzRules = self.getValidRule(clazz)
                if clazzRules:
                    rules = clazzRules;
        # 获取有效规则
        ruleList = self.filterRules(rules,attributes);
        validateResultList = [];

        for rule in ruleList:
            validators = rule.getValidators()
            validateResult = self.validateRule(rule,attributes,validators)
            validateResultList.append(validateResult)
            if validateResult.getResult() == False and not rule.getGoon():
                break;

        # 处理结果
        return self.resolveValidateResult(validateResultList)

    # 验证对象属性值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # param rules 验证规则
    # param attributes 验证值列表
    # param scenes 场景列表
    # param clearErrors 是否清除上次验证结果
    #
    def validateObject(self, object,rules = {}, scenes = [], clearErrors = True):

        attributes = ValidUtil.getAttrs(object)
        # 读取类的规则
        if not rules:
            clazzModule = inspect.getmodule(object.__class__).__name__;
            clazz = clazzModule + '.' + object.__class__.__name__
            clazzRules = self.getValidRule(clazz)
            if clazzRules:
                rules = clazzRules;

        return self.validate(rules,attributes,scenes,clearErrors);


    # 解析最终验证结果
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # param validateResultList 验证结果对象列表
    def resolveValidateResult(self,validateResultList = []):

        validResult = True

        for validateResult in validateResultList:
            if validateResult.getResult() == False:
                validResult = False
                self.addError(validateResult.getMessage())


        return validResult;

    def execValidator(self, rule = Rule,attributes = {}, validator = None):

        validator.setAttributes(attributes)
        # if isinstance(attributes,dict):
        #     values = rule.getAttrValues(attributes);
        #     result = validator.validateValues(values)
        # else:
        #     attrs = rule.getAttrs();
        #     result = validator.validateAttrs(attributes,attrs)

        return validator.validateRule(rule);

    # 单个规则验证
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # param validateResultList 验证结果对象列表
    def validateRule(self, rule = Rule,attributes = {},validatorConfs = []):

        operator = '&';
        if isinstance(validatorConfs[0],str):
            operator = validatorConfs.pop(0)

        validateResultList = [];
        for validatorConf in validatorConfs:
            # 递归
            if self.isResolveValidatorConf(validatorConf):
                validateResult = self.validateRule(rule,attributes,validatorConf)
                validateResultList.append(validateResult)
            else:
                validatorName = validatorConf.pop(0)
                validatorAttrs = {};
                if len(validatorConf) >= 1:
                    validatorAttrs = validatorConf.pop(0)

                if isinstance(validatorName, str):
                    nonsymbol = validatorName[0]
                    if nonsymbol == '!':
                        validatorName =  validatorName[1:]
                        validatorAttrs['non'] = True

                validator = self.createValidator(validatorName,validatorAttrs);
                validateResult = self.execValidator(rule,attributes,validator)
                validateResultList.append(validateResult)

        if operator == '&' or operator == 'and':
            return self.resolveAndRuleResult(validateResultList,rule)
        elif operator == '|' or operator == 'or':
            return self.resolveOrRuleResult(validateResultList, rule)
        else:
            return False

    def makeValidator(self,validatorRule):
        """
        :rtype:Validator
        :return:
        """
        validateType = validatorRule[0];
        try:
            validateConf = validatorRule[1]
        except IndexError:
            validateConf = {};

        return self.createValidator(validateType,validateConf);

    def createValidator(self,validateType = '',attrs = {}):
        """
        :rtype:Validator
        :return:
        """
        # validateType 类型为方法
        if isfunction(validateType) or isinstance(validateType,types.MethodType):
            attrsConf = attrs.copy();
            attrsConf['func'] = validateType
            validator = FuncValidator(attrsConf);
            validator.setValidation(self);
            return validator

        validatorConf = self.validators.get(validateType,None);

        if validatorConf is None:
            attrsConf = attrs.copy();
            validatorclazz = validateType
        else:
            validatorclazz = validatorConf.get("clazz")
            attrsConf = validatorConf.copy();
            attrsConf.update(attrs)
            attrsConf.pop('clazz')

        attrsConf['validatorName'] = validateType;

        # 验证器为外部函数
        if isfunction(validatorclazz) or isinstance(validatorclazz,types.MethodType):
            attrsConf['func'] = validatorclazz
            validator = FuncValidator(attrsConf);
            validator.setValidation(self);
            return validator;

        # 验证器为类对象
        if isinstance(validatorclazz,str) and validatorclazz.find('.') != -1:
            validatorclazz = __package__ + '.validator.' + validatorclazz

        validatorMeta = ValidUtil.getModuleMeta(validatorclazz)
        validator = validatorMeta(attrsConf);
        validator.setValidation(self);

        return validator

    # 获取有效的验证规则
    # <B> 说明： </B>
    # <pre>
    # 子类必须实现此方法
    # </pre>
    # param rules 验证规则列表
    # param scene 验证场景
    def filterRules(self,rules = [],scene = [],attributes = {}):

        ruleList = [];

        for ruleConf in rules:
            rule = Rule(ruleConf)
            if rule.isActive(scene,attributes):
                ruleList.append(rule)

        return ruleList

    def resolveAndRuleResult(self,validateResultList = [],rule = Rule):

        message = '';
        validResult = True;
        for validateResult in validateResultList:
            if validateResult.getResult() == False:
                validResult = False;
                message = validateResult.getMessage();
                break;
        if validResult == False:
            ruleMessage = rule.getMessage();
            if ruleMessage:
                message = ruleMessage;

            return ValidateResult(False,message, []);
        else:
            return ValidateResult(True, '', []);

    def resolveOrRuleResult(self,validateResultList = [],rule = Rule):

        message = '';
        validResult = False;
        for validateResult in validateResultList:
            if validateResult.getResult() == True:
                validResult = True;
                break;
            else:
                message = validateResult.getMessage();

        if validResult == False:
            ruleMessage = rule.getMessage();
            if ruleMessage:
                message = ruleMessage;

            return ValidateResult(False,message, []);
        else:
            return ValidateResult(True, '', []);

    # 是否继续解析验证器配置
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # param validatorConf 验证规则
    def isResolveValidatorConf(self,validatorConf = []):

        operatorCharacter = validatorConf[0];
        if isinstance(operatorCharacter,str):
            if operatorCharacter == '&' or operatorCharacter == '|':
                return True;

        elif isinstance(operatorCharacter,list):
            operator = operatorCharacter[0]
            if isinstance(operator,str) and (operator == '&' or operator == '|'):
                return True;
            elif isinstance(operator,list):
                return True

        return False

    def getDefaultMessage(self,validatorName):

        if validatorName in self.validators.keys():
            return self.validators[validatorName]['message']
        else:
            return ''

    # 新增验证器
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # param validatorName 验证器名称
    # param validatorClazz 验证器类名
    # param message 验证器错误消息提示
    def addValidator(self,validatorName,validatorClazz,message = ''):

        validatorAttrs = {
            'clazz': validatorClazz,
            'message': message
        };

        self.validators[validatorName] = validatorAttrs;

        return True

    # 调用验证器
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # param validatorName 验证器名称
    # param value 验证值
    # param attrs 验证器参数
    def callValidator(self,validatorName,value,*attrs,**kwattrs):

        validatorConf = self.validators.get(validatorName,None);
        if validatorConf is None:
            raise Exception(' validator {0}  is not exist'.format(validatorName))

        if attrs:
            validator = self.createValidator(validatorName,attrs[0])
        else:
            validator = self.createValidator(validatorName, kwattrs)

        return validator.validate(value);

    # 动态生成快捷验证器
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def registerShortcutValidator(self):

        for validatorName in self.validators:
            self.__createValidatorAliasMethod(validatorName)

    def __createValidatorAliasMethod(self,validatorName):

        import types;
        methodTemplate = """
def {methodName}(self,value,*attrs,**kwattrs):
    return self.callValidator('{methodName}',value,*attrs,**kwattrs)
        """
        methodCodeStr = methodTemplate.replace('{methodName}', validatorName);
        methodCode = compile(methodCodeStr, '', 'exec')
        functionCode = [c for c in methodCode.co_consts if isinstance(c, types.CodeType)][0]
        func = types.FunctionType(functionCode, {})
        func = types.MethodType(func, self)
        setattr(self, validatorName, func)
