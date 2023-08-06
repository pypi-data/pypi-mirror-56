# -*- coding: utf-8 -*-
from ..base.Validator import Validator
import re

"""
 * 数值范围验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['range',{min':6,'max':16}]],{'message'=>'请输入一个合法的6-16位数值'}]
* ['attrs',[['range',{min':6}]],{'message'=>'请输入一个大于等于6的数值'}]
 * ['attrs',[['range',{'max':16}]],{'message'=>'请输入一个小于等于16的数值'}]
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
class RangeValidator(Validator):

    def __init__(self,attrs):
        self.min = None
        self.max = None

        super().__init__(attrs)

    def validateValue(self,value,name = None):

        reg = r'^[-\+]?\d+(\.\d+)?$'
        if re.match(reg,str(value)) is None:
            return False

        result = True
        value = float(value)
        if self.min is not None:
            if value < self.min:
                result = False

        if self.max is not None:
            if value > self.max:
                result = False

        if result:
            return True
        else:
            self.addParams({
                'min': self.min,
                'max': self.max
            })

        return result;

