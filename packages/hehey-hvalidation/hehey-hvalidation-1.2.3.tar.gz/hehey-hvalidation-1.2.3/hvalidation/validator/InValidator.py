# -*- coding: utf-8 -*-
from ..base.Validator import Validator
from ..utils.ValidUtil import ValidUtil

"""
 * in 集合验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['inlist',{'numbers':[1,2,3]}]],{'message'=>'输入的值必须为1,2,3,4'}]
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
class InValidator(Validator):

    def __init__(self,attrs):
        self.numbers = []

        super().__init__(attrs)
        self.numbers = ValidUtil.listToStr(self.numbers)

    def validateValue(self,value,name = None):

        self.addParam('numbers', ','.join(self.numbers));
        if str(value) in self.numbers:
            return True
        else:
            return False

