# -*- coding: utf-8 -*-
from ..base.Validator import Validator
import re

"""
 * 邮箱验证器
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
class EmailValidator(Validator):


    def __init__(self,attrs):
        self.pattern = r"^[a-zA-Z0-9!#$%&'*+\\/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+\\/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?$"

        self.fullPattern = r"^[^@]*<[a-zA-Z0-9!#$%&'*+\\/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+\\/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?>$"

        self.allowName = False;

        super().__init__(attrs)

    def validateValue(self,value,name = None):

        value = str(value)

        if re.match(self.pattern,value) is not None or (self.allowName or re.match(self.fullPattern,value) is not None):
            return True
        else:
            return False
