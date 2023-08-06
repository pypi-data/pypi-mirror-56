# -*- coding: utf-8 -*-
from ..base.Validator import Validator
import re
"""
 * 正则验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['reg',{'pattern':'^1[0-9]{1}\d{9}$'}]],{'message'=>'你输入的手机号格式错误！'}]
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
class RegularValidator(Validator):


    def __init__(self,attrs):

        super().__init__(attrs)
        self.pattern = ''

    def validateValue(self,value,name = None):

        if re.match(self.pattern,str(value)) is None:
            return False
        else:
            return True

