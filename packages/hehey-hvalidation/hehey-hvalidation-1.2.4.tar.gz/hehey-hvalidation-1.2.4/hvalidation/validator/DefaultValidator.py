# -*- coding: utf-8 -*-
from ..base.Validator import Validator

"""
 * 默认验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['email']],{'message'=>'你输入的邮箱格式错误！'}]
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
class DefaultValidator(Validator):


    def __init__(self,attrs):

        super().__init__(attrs)

    def validateValue(self,value,name = None):

        pass
