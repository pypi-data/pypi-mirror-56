# -*- coding: utf-8 -*-
from ..base.Validator import Validator
import re
"""
 * 浮点数验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:decimalPoint 保留的小数点位数
 * ['attrs',[['float',{'decimalPoint':2}]],{'message'=>'你输入的值必须为浮点数'}]
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
class FloatValidator(Validator):


    def __init__(self,attrs):
        self.decimalPoint = 2
        self.pattern = r'^[-\+]?(([1-9]{1}\d*)|([0]{1}))(\.(\d){point})?$'
        super().__init__(attrs)

    def validateValue(self,value,name = None):

        if not self.decimalPoint:
            point = '+'
        else:
            point = '{1,' + str(self.decimalPoint) + '}'

        pattern = self.pattern.replace('{point}',point)

        if re.match(pattern,str(value)) is None:
            return False
        else:
            return True