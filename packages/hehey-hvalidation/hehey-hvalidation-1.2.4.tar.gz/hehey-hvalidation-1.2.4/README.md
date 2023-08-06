# hehey-hvalidation

#### 介绍
hehey-hvalidation 是一个python 全面的验证器工具类。
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
ruleConf = {
    "goon":False,# 当验证错误是是否继续验证
    "message":"你输入的格式错误!",# 错误消息
    "on":"create",# 使用场景
    "when":'valint(方法或函数)',# 满足条件
};

# 验证器参数
validatorConf = {
    "message":"你输入的格式错误!",# 错误消息
    "skipOnEmpty":"create(方法或函数)",# 验证值为空时是否调用验证
    "emptyFunc":"emptyFunc(方法或函数)",# 验证是否空方法,可以重写
    "non":False,# 结果是否非
    "when":'valint()',# 满足条件
};


```
#### 基本示例
- 快速使用
```python
from hvalidation.validation import Validation
validation = Validation()

validateData = {
    'username': 'hehe',
    'userid': 10,
    'title': 'hehe 每天小酌一杯',
    'age': 10,
    'birthday':'1988-06-14',
    'tel':'13511221111',
    'password':'5241411',
    'confirmpassword':'2541414',
    'sceneType':"login",
};

validateRules = [
    ['username',[ ['required'],['alphaNum'] ],{'message':'请输入的字符必须包含字母字符'}],
    ['userid',[ ['!empty'],['int'] ],{'message':'user_id 必须为数字'}],
    ['title',[ ['required'],['len',{"min":2,"max":200}] ],{'message':'请输入一个长度介于 {min} 和 {max} 之间的字符串'}],
    ['age',[ ['required'],['range',{"min":2,"max":200}] ],{'message':'请输入一个合法的{min}-{max}数值'}],
    ['birthday',[ ['required'],['date',{"format":'Y-m-d'}] ],{'message':'你输入的日期格式错误,正确日期格式为:{format}'}],
    ['tel',[ ['required'],['date',{"format":'Y-m-d'}] ],{'message':'你的输入手机格式有误,必须11位'}],
    ['password',[ ['required'],['alphaDash',{"len":[6,15]}] ],{'message':'请输入的字符包含字母、数字、破折号（ - ）以及下划线（ _ ）,字符长度在6-15 位'}],
    ['confirmpassword',[ ['required'],['alphaDash',{"len":[6,15]}], ['eqstrfield',{'field':"password"}] ],{'message':'你的输入确认密码与密码不一致!'}],
    ['sceneType',[ ['required'],['enum',{"numbers":['login','changeTel','reg']}], ],{'message':'你输入的场景类型错误,必须为{numbers}!'}],
    
];

if not validation.validate(validateData,validateRules):
    print("验证错误:{0}".format(validation.getFirstError()))
else:
    print('验证通过!')

```

- 接入hehey 组件
```python
# settings.py 配置文件
components = {
    'validation': {
        'clazz': 'hvalidation.validation.Validation',
     },
}

from hehe import he

validateData = {
    'username': 'hehe',
};

validateRules = [
    ['username',[ ['required'],['alphaNum'] ],{'message':'请输入的字符必须包含字母字符'}],
];

if not he.app.validation.validate(validateData,validateRules):
    print("验证错误:{0}".format(he.app.validation.getFirstError()))
else:
    print('验证通过!')

```

- 多个验证器
```python
validateRules = [
    ['title',[ ['required'],['len',{"min":2,"max":200}] ],{'message':'请输入一个长度介于 {min} 和 {max} 之间的字符串'}],
];

```

- 验证多个属性
```python
validateRules = [
    [['userid','username'],[['!empty']],{'message':'参数不能为空'}],
];
```

- 验证多维数组
```python
validateRules = [
    [['user.userid'],[['!empty']],{'message':'参数不能为空'}],
];
```

- 多个验证器支持与或 or,and,&,|
```python
validateRules = [
    ['username',[['!empty'],['minlen',{'number':1}]],{'message':'请输入一个10-20位的字符串'}],
    ['age',['and',['int'],['minlen',{'number':10}]],{'message':'你的输入的年龄有误,年龄必须超过10 岁！'}],
    ['age1',['or',['int'],['minlen',{'number':10}]],{'message':'你的输入的年龄有误,年龄必须超过10 岁！'}],
];
```

- 设置验证规则错误消息
```python

validateRules = [
    ['username',[['!empty']],{'message':'不能为空'}],
];

```

- 设置验证器错误消息
```python
validateRules = [
    ['age',[['!empty'],['minlen',{'number':1,"message":"请输入的值必须大于1"}]],{'message':'不能为空'}],
];

```

- 设置验证规则使用场景
```python
validateRules = [
    ['username',[['!empty'],['minlen',{'number':1}]],{'message':'请输入一个10-20位的字符串','on':['create','update','login']}],
];
```

- 设置验证规则的前置条件
```python
def validint(value,name,validator):

    if isinstance(value,int):
        return True

    else:
        return False


validateRules = [
    ['userid',[['!empty']],{'message':'你输入格式错误','when':validint}],
];

```

- 添加自定义验证器
```python
from hvalidation.validation import Validation
validation = Validation()
validation.addValidator("ip6",'app.utils.IpValidator.IpValidator','请输入ip格式')

validateRules = [
    ['userip',[['!empty'],['ip6']],{'message':'你输入格式错误'}],
];

```

- 验证器直接为方法或函数
```python

def validint(value,name,validator):

    if isinstance(value,int):
        return True

    else:
        return False


validateRules = [
    ['userid',[['!empty'],[validint]],{'message':'请输入一个整型数值'}],
];

```

- 直接使用验证器验证
```python
from hvalidation.validation import Validation
validation = Validation()
# 验证ip6 
validation.ip('102.021.054.11',mode = 'ip6');

```

- 装饰器注册验证器
```python
from hvalidation.validation import reg_validator

# 注册函数方法验证器 
@reg_validator('用户名不能为空','可定义验证器别名,可不填')
def username(self,value,name = None):

    if value:
        return True
    else:
        return False;



# 注册类验证器,创建文件IpValidator.py
from hvalidation.base.Validator import Validator
import re;
@reg_validator('ip 格式有误','ip')
class IpValidator(Validator):

    def __init__(self,attrs,validation = None):
        self.pattern = r'^(\d+\.\d+\.\d+\.\d+)$'
        super().__init__(attrs,validation)


    def validateValue(self,value,name = None):

        if re.match(self.pattern, value) is not None:
            return True
        else:
            return False


```

- 装饰器注册验证规则
```python
from hvalidation.validation import Validation,reg_valid_rule

class Address:
    @reg_valid_rule("ip", property="myuser", attrs={"message": "hehe"})
    @reg_valid_rule("float", property="myuser", attrs={"message": "hehe"})
    def __init__(self):

        self.myuser = "什么规则"

validation = Validation()
address = Address()
if not validation.validate(address):
    print("验证错误:{0}".format(validation.getFirstError()))
else:
    print('验证通过!')
    
#或

if not validation.validateObject(address):
    print("验证错误:{0}".format(validation.getFirstError()))
else:
    print('验证通过!')


```


### 默认验证器
验证器 | 说明 | 规则示例
----------|-------------|------------
`required`  | 必填字段 | `['fieldname', ['required'] ]`
`empty`  | 不为空字段,常配合!使用 | `['fieldname', ['empty'] ]`，`['fieldname', ['!empty'] ]`
`float`  | 数值必须为浮点数,即整型,或带小数点的数值 | `['fieldname', ['float'] ]`
`int`  | 数值必须为整型 | `['fieldname', ['int'] ]`
`boolean`  | 数值必须为布尔值,True or False | `['fieldname', ['boolean'] ]`
`tel`  | 11 位手机号 | `['fieldname', ['tel'] ]`
`date`  | 验证日期格式 | `['fieldname', ['date',{"format":'Y-m-d'}] ]`
`rangedate`  | 验证日期范围 | `['fieldname', ['date',{"min":'2019-10-10','max':'2010-10-11'}] ]`
`email`  | 验证邮箱格式 | `['fieldname', ['email'] ]`
`ip`  | 验证ip格式,支持mode 格式 ip4,ip6 | `['fieldname', ['ip',{"mode":"ip4"}]`
`ip4`  | 验证ip4格式 | `['fieldname', ['ip4']]`
`ip6`  | 验证ip6格式 | `['fieldname', ['ip6']]`
`url`  | 验证url 地址格式,支持设置defaultScheme | `['fieldname', ['url',{"defaultScheme":"https"}]]`
`range`  | 验证数值范围大小 | `['fieldname', ['range',{"min":10,'max':20}] ]`
`compare`  | 比较指定数值大小,支持操作符,'gt','egt','lt','elt','eq','>','>=','<','<=','=' | `['fieldname', ['compare',{"number":10,"operator":"gt"}] ]`
`eq`  | 验证数值相等,compare 操作符 eq 的简写  | `['fieldname', ['eq',{"number":1}]]`
`gt`  | 验证数值大于,compare 操作符 gt 的简写  | `['fieldname', ['gt',{"number":1}]]`
`egt`  | 验证数值大于等于,compare 操作符 egt 的简写  | `['fieldname', ['egt',{"number":1}]]`
`lt`  | 验证数值小于,compare 操作符 lt 的简写  | `['fieldname', ['lt',{"number":1}]]`
`elt`  | 验证数值小于等于,compare 操作符 elt 的简写  | `['fieldname', ['elt',{"number":1}]]`
`minlen`  | 验证字符最小长度  | `['fieldname', ['minlen',{"number":1}]]`
`maxlen`  | 验证字符最大长度  | `['fieldname', ['maxlen',{"number":1}]]`
`len`  | 验证字符最大范围  | `['fieldname', ['maxlen',{"min":1,"max":100}]]`
`currency`  | 验证货币数值,比如0.51,支持设置小数点位数decimalPoint  | `['fieldname', ['maxlen',{"decimalPoint":2}]]`
`ch`  | 验证中文格式 | `['fieldname', ['ch']]`
`en`  | 验证英文格式 | `['fieldname', ['en']]`
`alpha`  | 验证包含字母字符[a-z_A-Z]格式 | `['fieldname', ['alpha']]`
`alphaNum`  | 验证包含字母、数字格式 | `['fieldname', ['alphaNum']]`
`alphaDash`  | 验证字母、数字、破折号（ - ）以及下划线（ _ ）格式 | `['fieldname', ['alphaDash']]`
`inlist`  | 输入的值必须包含在指定的列表 | `['fieldname', ['inlist']]`
`enum`  | 输入的值必须包含在指定的列表 | `['fieldname', ['enum']]`
`notin`  | 输入的值必须不包含在指定的列表 | `['fieldname', ['notin']]`
`vlist`  | 验证列表里每个元素的类型 | `['fieldname', ['vlist',[ ['int'],['minlen'] ]]]`
`eqstrfield`  | 验证字段与指定字段值是否相等 | `['fieldname', ['eqstrfield',{"field":"confirmpassword"}]]]`
`eqintfield`  | 验证字段与指定字段数值是否相等 | `['fieldname', ['eqintfield',{"field":"age"}]]]`
`gtintfield`  | 验证字段与指定字段数值是否大于 | `['fieldname', ['gtintfield',{"field":"age"}]]]`
`egtintfield`  | 验证字段与指定字段数值是否大于等于 | `['fieldname', ['egtintfield',{"field":"age"}]]]`
`ltintfield`  | 验证字段与指定字段数值是否小于 | `['fieldname', ['ltintfield',{"field":"age"}]]]`
`eltintfield`  | 验证字段与指定字段数值是否小于等于 | `['fieldname', ['eltintfield',{"field":"age"}]]]`
`gtdatefield`  | 验证日期字段与指定日期字段数值是否大于 | `['enddate', ['gtdatefield',{"field":"startdate"}]]]`
`egtdatefield`  | 验证日期字段与指定日期字段数值是否大于等于 | `['enddate', ['egtdatefield',{"field":"startdate"}]]]`
`ltdatefield`  | 验证日期字段与指定日期字段数值是否小于 | `['enddate', ['ltdatefield',{"field":"startdate"}]]]`
`eltdatefield`  | 验证日期字段与指定日期字段数值是否小于等于 | `['enddate', ['eltdatefield',{"field":"startdate"}]]]`