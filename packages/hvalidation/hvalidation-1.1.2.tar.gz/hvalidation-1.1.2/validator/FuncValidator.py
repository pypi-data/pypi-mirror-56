# -*- coding: utf-8 -*-
from ..base.Validator import Validator
"""
 * 函数验证器
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
class FuncValidator(Validator):

    def __init__(self,attrs):
        self.func = ''
        super().__init__(attrs)


    def validateValue(self,value,name = None):

        return self.func(value,name,self);

