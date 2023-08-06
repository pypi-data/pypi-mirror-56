# -*- coding: utf-8 -*-
from ..base.Validator import Validator

"""
 * 布尔值类型验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['boolean']],{'message'=>'你输入的值非布尔值类型'}]
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
class BooleanValidator(Validator):

    def validateValue(self,value,name = None):

        if isinstance(value,bool):
            return True
        else:
            return False

