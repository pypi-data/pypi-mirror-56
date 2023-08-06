# hehey-hvalidation

#### 介绍
hehey-hvalidation 是一个python 全面的验证器工具类.
其主要特点有:
  - 支持常用验证器
  - 验证器易扩展
  - 支持验证字典以及对象属性
  - 示例全面
  
#### 依赖以及版本要求
- python >= 3.5

#### 安装
- 直接下载:
```

```
- 命令安装：
```
pip install hehey-hvalidation
```
#### 基础文件以目录


#### 参数配置
```python

# 验证器规则参数


# 验证器参数



```
#### 基本示例
- 快速使用
```python
from 


```

- 接入hehey 组件
```python


```

- 多个验证器
```python


```

- 验证多个属性
```python

```

- 多个验证器支持与或 or,and,&,|
```python

```

- 设置验证规则错误消息
```python

```

- 设置验证器错误消息
```python

```

- 设置验证规则使用场景
```python

```

- 设置验证规则的前置条件
```python

```

- 添加自定义验证器
```python

```

- 验证器直接为方法或函数
```python

```

- 直接使用验证器验证
```python

```

- 装饰器注册验证器
```python

```

- 装饰器注册验证规则
```python

```


- 默认验证器
验证器 | 说明 | 基础示例
----------|-------------|------------
`required`  | 要求此字段/属性是必须的(不为空的)。[关于为空](#about-empty-value) | `['tagId, userId', 'required' ]`
`int/integer`   | 验证是否是 int **支持范围检查** | `['userId', 'int']` `['userId', 'int', 'min'=>4, 'max'=>16]`
