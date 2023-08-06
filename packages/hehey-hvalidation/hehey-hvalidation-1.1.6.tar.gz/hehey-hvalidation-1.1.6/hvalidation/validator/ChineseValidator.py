# -*- coding: utf-8 -*-
from ..base.Validator import Validator
import re
"""
 * 中文字符号验证器
 *<B>说明：</B>
 *<pre>
 * 11 位手机验证格式
 * 规则格式:
 * ['attrs',[['ch']],{'message'=>'请输入字符必须为中文！'}]
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
class ChineseValidator(Validator):


    def __init__(self,attrs):
        self.pattern = r'^[\x{4e00}-\x{9fa5}]+$'
        super().__init__(attrs)

    def validateValue(self,value,name = None):

        if re.match(self.pattern,str(value)) is None:
            return False
        else:
            return True

        English

