# -*- coding: utf-8 -*-
from ..base.Validator import Validator

"""
 * 字符串长度验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['length',{number':15,'operator':'gt'}]],{'message'=>'请输入一个长度大于15的数值'}]
 * operator:大于(gt),大于等于(egt),小于(lt),小于等于(elt)
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
class LengthValidator(Validator):

    def __init__(self,attrs):
        self.number = 0
        self.operator = ''
        self.operatorList = ['gt','egt','lt','elt','eq','>','>=','<','<=','=']

        super().__init__(attrs)

    def validateValue(self,value,name = None):
        self.addParam('number',self.number);

        if self.operator not in self.operatorList:
            return False

        result = False
        valueLen = len(str(value).encode('utf-8'))

        if self.operator == 'gt' or self.operator == '>':
            # 大于
            result = (valueLen > self.number)
        elif self.operator == 'egt' or self.operator == '>=':
            # 大于等于
            result = (valueLen >= self.number)
        elif self.operator == 'lt' or self.operator == '<':
            # 小于
            result = (valueLen < self.number)
        elif self.operator == 'elt' or self.operator == '<=':
            # 小于等于
            result = (valueLen <= self.number)
        elif self.operator == 'eq' or self.operator == '=':
            # 小于等于
            result = (valueLen == self.number)
        else:
            pass


        return result