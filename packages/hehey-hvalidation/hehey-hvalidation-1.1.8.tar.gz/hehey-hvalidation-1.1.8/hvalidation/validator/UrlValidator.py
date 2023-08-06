# -*- coding: utf-8 -*-
from ..base.Validator import Validator
import re
"""
 * url 网址验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['url']],{'message'=>'请输入一个合法的网络地址！'}]
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
class UrlValidator(Validator):

    def __init__(self,attrs):
        self.pattern = r'^{schemes}:\/\/(([A-Z0-9][A-Z0-9_-]*)(\.[A-Z0-9][A-Z0-9_-]*)+)'
        self.schemes = ['http', 'https'];
        self.defaultScheme = '';
        super().__init__(attrs)

    def validateValue(self,value,name = None):
        value = str(value)
        if not self.defaultScheme and  value.find('://') != -1:
            value = self.defaultScheme + '://' + value

        if value.find(self.pattern) != -1:
            pattern = self.pattern.replace("{schemes}",'(' + "|".join(self.schemes) + ')')
        else:
            pattern = self.pattern

        if re.match(pattern,value) is None:
            return False
        else:
            return True

