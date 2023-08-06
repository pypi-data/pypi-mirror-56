# hehey-hcontainer

#### 介绍
hehey-hcontainer 是一个python di 容器,提供依赖注入等等功能

#### 依赖以及版本要求
- python >= 3.5

#### 安装
- 直接下载:
```

```
- 命令安装：
```
pip install hehey-hcontainer
```
#### 基础文件以目录


#### 参数配置
```python
from hcontainer.base.Definition import Definition
beanConf = {
    'class':'site.service.User.User', # 类路径
    '_single': True, # 是否单例,默认是单例,
    '_scope': 'app', # 对象作用域, app应用作用域，request 请求作用域
    '_init': 'init', # 初始化方法, 对象创建后调用设置的方法(设置属性完成后调用)
    '_args': [], # or True 构造方法参数，支持索引，关联数组
    '_attr': [], # 类其他属性，直接注入
    'attr1':'属性1',
    'attr2':'属性2',
    'attrBean':'<func::bean>',# 属性调用函数, 自动调用func函数(bean) 获取属性值,
    'addresstBean':'<ref::address|天收你>',# 属性对应另一个bean(user),| 之后为bean 的参数
    'attr3':Definition({
        '_ref':'user' # attr3 为另一个bean为user的对象
    })
}


```
#### 基本示例
- 快速使用
```python
from hcontainer.bean import BeanManager
components = {
        # 构造器注入
        'user':{
            'clazz': 'site.service.User.User',
            '_args':[
                'hehe 小酌一杯'
            ],
        },

        # 属性注入
        'address':{
            'clazz':'site.service.Address.Address',
            'realName':'hehe',
            'user':'<ref::user>'
        },

}

beanManager = BeanManager.make(components);

# 获取bean 实例
user = beanManager.getBean('user')
address = beanManager.getBean('address')

```

- 属性注入
```python
from hcontainer.bean import BeanManager
class User:

    def __init__(self,**attrs):
    
        self.username = ''
        
        if attrs:
            #设置属性
            pass
            
        return ;

    def getUsername(self):

        return self.username
        
components = {
    # 构造器注入
    'user':{
        'clazz': 'site.service.User.User',
        'username':'hehe',
    },
}



beanManager = BeanManager.make(components);
user = beanManager.getBean('user')


```

- 构造参数注入
```python

# 示例1
class User:

    def __init__(self,**attrs):
    
        self.username = ''
        
        if attrs:
            #设置属性
            pass
        
        self._init();
        return ;
    
    def _init(self):
        # 初始化操作
        return;

    def getUsername(self):

        return self.username

# 此配置针对构造参数只有**attrs 
components = {
    # 构造器注入
    'user':{
        'clazz': 'site.service.User.User',
         '_args':True,
        'username':'hehe',
    },
}

# 示例2
class Address:

    def __init__(self,address='',city = ''):
        self.addr = address
        self.city = city
        self._user = None;

    @property
    def user(self):
        return self._user

components = {
    # 构造器注入
    'user':{
        'clazz': 'site.service.User.User',
        '_args':[
            '我的收货详细地址',
            '上海'
        ],
    },
}

```

- bean 属性值为另一bean 
```python

from hcontainer.bean import BeanManager

class User:
    
    def __init__(self):
    
        self.username = ''
        self.address = None;
        return ;
    
    def getAddress(self):

        return self.address

class Address:
    def __init__(self,address='',city = ''):
        self.addr = address
        self.city = city

    def getAddr(self):
        return self.addr

components = {
        'user':{
            'clazz': 'site.service.User.User',
            'username':"hehe 小酌一杯",
            'address':'<ref::address>'
        },

        # 属性注入
        'address':{
            'clazz':'site.service.Address.Address',
            'address':'深圳',
            'city':'上海',
        }
}

beanManager = BeanManager.make(components);
user = beanManager.getBean('user')
address = user.getAddress()
address.getAddr()


```

- 初始化方法(对象创建后,自动调用指定的方法)
```python
class User:

    def __init__(self,**attrs):
    
        self.username = ''
        
        if attrs:
            #设置属性
            pass
        
        self._init();
        return ;
    
    def _init(self):
        # 初始化操作
        print("初始化对象自动调用此方法!")
        return;

    def getUsername(self):

        return self.username

components = {
    # 构造器注入
    'user':{
        'clazz': 'site.service.User.User',
        '_init':"_init",
        'username':'hehe',
    },
}


```

- 装饰器注解(id,ref)类为bean 对象
```python
from hcontainer.bean import BeanManager
from hcontainer import bean

@bean.id("addrbean")
class Address:

    def __init__(self,address=''):
        self.addr = address

    def getAddr(self):
        return self.addr

@bean.id("userbean")
class User:

    def __init__(self,username = 'nnnn'):
        self.username = username
        self.__address = None;
    
    @property
    @bean.ref('addrbean',name='__address')
    def address(self):
        return self.__address    

    def getName(self):

        return self.username

beanManager = BeanManager.make();
user = beanManager.getBean('user')

```

- 创建新的bean 实例
```python
from hcontainer.bean import BeanManager
components = {
    # 构造器注入
    'user':{
        'clazz': 'site.service.User.User',
        '_init':"_init",
        'username':'hehe',
    },
}

beanManager = BeanManager.make(components);
# 新对象,非单例
user = beanManager.makeBean('user')

```
- 根据类路径创建bean 对象
```python
from hcontainer.bean import BeanManager
beanManager = BeanManager.make();
user = beanManager.getBean('site.service.User.User')

```

- bean 作用域
```python


```

- 创建bean容器
```python
from hcontainer.bean import BeanManager
beanManager = BeanManager.make();
requestContainer = beanManager.makeContainer('request')
sessionContainer = beanManager.makeContainer('session')

```











