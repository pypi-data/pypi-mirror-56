# -*- coding: utf-8 -*-
from ..base.Validator import Validator
import time
"""
 * 日期验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['date',{'format':'Y-m-d'}]],{'message'=>'你输入的日期格式错误,正确日期格式为:{format}'}]
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
class DateValidator(Validator):

    def __init__(self,attrs):
        self.format = 'Y-m-d'
        super().__init__(attrs)


    def validateValue(self,value,name = None):

        try:
            time.strptime(value, self.format)
            self.addParam('format',self.format)
            return True
        except:
            return False