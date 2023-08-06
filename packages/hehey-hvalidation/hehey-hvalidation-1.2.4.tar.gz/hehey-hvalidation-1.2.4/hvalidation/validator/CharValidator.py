# -*- coding: utf-8 -*-
from hehe.core.hvalidation.base.Validator import Validator
import re
"""
 * 字符验证器
 *<B>说明：</B>
 *<pre>
 * 略
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
class CharValidator(Validator):

    def __init__(self,attrs):
        self.mode = 'alpha'
        self.len = []
        self.patterns = {
            "alpha":r'^(?:[a-zA-Z]{point})$',
            "alphaNum":r'^(?:[a-zA-Z0-9]{point})$',
            "alphaDash": r'^(?:[\w-]{point})$'
        }

        super().__init__(attrs)

    def validateValue(self,value,name = None):

        if not self.len:
            point = '+'
        else:
            point = '{'+str(self.len[0]) + ',' + str(self.len[1]) +'}'

        pattern = self.patterns.get(self.mode,None)
        pattern = pattern.replace('{point}', point)
        if re.match(pattern,str(value)) is None:
            return False
        else:
            return True


