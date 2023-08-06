# -*- coding: utf-8 -*-
from ..base.Validator import Validator

"""
 * 验证list 元素的值类型
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['vlist',{'numbers':[1,2,3]}]],{'message'=>'输入的值必须为1,2,3,4'}]
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
class ListValidator(Validator):

    def __init__(self,attrs):
        self.validators = [];# 验证器
        super().__init__(attrs)

    def validateValue(self,value,name = None):

        result = True;
        for val in value:
            for validatorRule in self.validators:
                validator = self.validation.makeValidator(validatorRule);
                result = validator.validateValue(val,name)
                if result is False:
                    result = False;
                    break;
            if result is False:
                break


        return result;

