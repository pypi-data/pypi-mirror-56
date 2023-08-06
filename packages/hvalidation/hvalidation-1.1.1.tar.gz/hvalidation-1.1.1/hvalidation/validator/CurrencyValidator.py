# -*- coding: utf-8 -*-
from ..base.Validator import Validator
import re
"""
 * 货币验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['currency']],{'message'=>'请输入一个合法的货币类型数值！'}]
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
class CurrencyValidator(Validator):

    def __init__(self,attrs):
        self.pattern = r'^[-\+]?(([1-9]{1}\d*)|([0]{1}))(\.(\d){1,{point}})?$'
        self.decimalPoint = 2;
        super().__init__(attrs)

    def validateValue(self,value,name = None):
        value = str(value)
        self.addParams('{point}',self.decimalPoint)
        if value.find(self.pattern) != -1:
            pattern = self.pattern.replace("{point}",'(' + "|".join(self.decimalPoint) + ')')
        else:
            pattern = self.pattern

        if re.match(pattern,value) is None:
            return False
        else:
            return True

