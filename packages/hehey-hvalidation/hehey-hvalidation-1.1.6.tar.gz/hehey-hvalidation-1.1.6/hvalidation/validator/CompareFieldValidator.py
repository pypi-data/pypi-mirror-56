# -*- coding: utf-8 -*-
from ..base.Validator import Validator
from ..utils.ValidUtil import ValidUtil
"""
 * 字段值比较验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['range',{number':6,'operator':'gt'}]],{'message'=>'请输入一个大于15的数值'}]
 * operator:大于(gt),大于等于(egt),小于(lt),小于等于(elt)
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
class CompareFieldValidator(Validator):

    def __init__(self,attrs):

        self.field = '' # 比较的字段startdate,userid
        self.comparetype = 'int' # 比较类型int,str,date
        self.operator = ''# 比较的操作符 gt edt lit 等等
        self.operatorList = ['gt','egt','lt','elt','eq','>','>=','<','<=','=']

        super().__init__(attrs)

    def getFormatValue(self,value):

        if self.comparetype == 'int':
            return float(value)
        elif self.comparetype == 'date':
            return ValidUtil.strtotime(value);
        elif self.comparetype == 'str':
            return str(value)
        else:
            return int(value)

    def validateValue(self,value,name = None):

        self.addParam('field2',name);
        self.addParam('field1', self.field);

        comparefieldValue = self.getFormatValue(self.getAttribute(self.field))

        if self.operator not in self.operatorList:
            return False

        result = False
        validValue = self.getFormatValue(value)

        if self.operator == 'gt' or self.operator == '>':
            # 大于
            result = (validValue > comparefieldValue)
        elif self.operator == 'egt' or self.operator == '>=':
            # 大于等于
            result = (validValue >= comparefieldValue)
        elif self.operator == 'lt' or self.operator == '<':
            # 小于
            result = (validValue < comparefieldValue)
        elif self.operator == 'elt' or self.operator == '<=':
            # 小于等于
            result = (validValue <= comparefieldValue)
        elif self.operator == 'eq' or self.operator == '=':
            # 小于等于
            result = (validValue == comparefieldValue)
        else:
            pass

        return result