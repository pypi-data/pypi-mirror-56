# -*- coding: utf-8 -*-
from ..base.Validator import Validator
import re
"""
 * 比较值验证器
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
class CompareValidator(Validator):

    def __init__(self,attrs):
        self.number = 0
        self.operator = ''
        self.operatorList = ['gt','egt','lt','elt','eq','>','>=','<','<=','=']

        super().__init__(attrs)

    def validateValue(self,value,name = None):
        self.addParam('number',self.number);

        reg = r'^[-\+]?\d+(\.\d+)?$/'
        if re.match(reg,value) is None:
            return False

        if self.operator not in self.operatorList:
            return False

        result = False
        value = float(value)

        if self.operator == 'gt' or self.operator == '>':
            # 大于
            result = (value > self.number)
        elif self.operator == 'egt' or self.operator == '>=':
            # 大于等于
            result = (value >= self.number)
        elif self.operator == 'lt' or self.operator == '<':
            # 小于
            result = (value < self.number)
        elif self.operator == 'elt' or self.operator == '<=':
            # 小于等于
            result = (value <= self.number)
        elif self.operator == 'eq' or self.operator == '=':
            # 小于等于
            result = (value == self.number)
        else:
            pass

        return result