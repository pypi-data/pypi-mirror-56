# -*- coding: utf-8 -*-
from ..base.Validator import Validator
"""
 * 必填验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['required']],{'message'=>'你输入的值不能为空'}]
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
class RequiredValidator(Validator):

    def __init__(self,attrs):
        super().__init__(attrs)
        self.skipOnEmpty = False


    def validateValue(self,value,name = None):
        if self.isEmpty(value):
            return False
        else:
            return True