# -*- coding: utf-8 -*-

from .base.Container import Container
from .base.Definition import Definition
import inspect

# 标识类为bean组件装饰器
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def id(beanId = '',**definition):

    def decorator(bean):
        clazzModule = inspect.getmodule(bean).__name__;
        clazzBean = clazzModule + '.' + bean.__name__
        beanConf = {
            'clazz': clazzBean,
        }

        if beanId:
            beanConf['id'] = beanId
        beanConf.update(definition)
        BeanManager.registerBeanComponent(clazzBean,beanConf)

        return bean


    return decorator

# 标识类属性为其他bean组件对象装饰器
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def ref(beanId,**beanConf):

    def decorator(property):
        clazzModule = inspect.getmodule(property).__name__
        clazzBean = clazzModule + '.' + property.__qualname__.split('.')[0];
        propertyName = property.__name__;
        beanConf['clazz'] = clazzBean
        realName = beanConf.pop('name',None)
        if realName:
            beanConf[realName] = '<ref::'+beanId+'>'
        else:
            beanConf['__' + propertyName] = '<ref::' + beanId + '>'

        BeanManager.registerBeanComponent(clazzBean, beanConf)

        return property

    return decorator

# 创建容器管理器对象
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def make()->'BeanManager':

    return BeanManager.make()



"""
 * 容器管理器
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  bean 组件基本配置
    components = {

        'user':{
            'clazz': 'site.service.User.User',
            '_args':[
                '你想什么'
            ],
        },
        
        'addressuser':{
            'clazz':'site.service.Address.Address',
            'addr':'xxxxx',
            'user':'<ref::user>'
        },

        'address':{
            'clazz':'site.service.Address.Address',
            'addr':'xxxxx',
            'user':'<hehe.common.func.hbean::user>'
        }
    }
 
    address = he.getBean("address")
    
    user = he.getBean("user")
    
    
    常用格式
    
    {
        'class'：'site.service.User.User',// 类路径
        '_single':True, // 是否单例 默认是单例,
       '_scope':'app',// 对象作用域,app 应用级别，forever 永远不失效
       '_init':'init',// 初始化方法,对象创建后调用设置的方法(设置属性完成后调用)
        '_args':[], // 构造方法参数，支持索引，关联数组
        '_attrs':[] // 类其他属性，直接注入
       'attr1'：'26',
       'attr2'：'',
       'attrBean'：'<func::user>',属性调用函数,自动调用func函数,函数参数为account
       'account'：'<ref::account|1>'
       'name57'：Definition([
       '_ref'：'account',// name57 为另一个bean 为account 的对象
       ]),
  }
 
 
 class Address:
    addr = '地址市什么柜子'
    user = None
    def __init__(self,user:User='<ref::user>',address='address'):
        self.addr = address
        self.user = user;
        
    def getName(self,cond):

        return 'address:' + self.addr + str(random.randint(0,10))
    
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
class BeanManager():

    SCOPE_REQUEST = 'request';

    CLASS_KEY_NAME = "clazz";

    # 当前对象
    # <B> 说明： </B>
    # <pre>
    # app 应用级别,应用启动,开始生效
    # request 请求级别,每次请求时生效,请求结束后失效
    # </pre>
    manager = None;

    # 类bean定义
    # <B> 说明： </B>
    # <pre>
    # 通过类装饰器定义的bean 配置,以类路径为key
    # </pre>
    clazzBeanComponents = {}


    # 构造器
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def __init__(self,components = {}):
        """ 定义属性　"""

        # 容器列表
        # <B> 说明： </B>
        # <pre>
        # app 应用级别,应用启动,开始生效
        # request 请求级别,每次请求时生效,请求结束后失效
        # </pre>
        self.scopeContainer = {}

        # bean定义对象列表
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.definitions = {}

        # bean 组件配置
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.components = components

        # 类与bend id 的对应关系
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.clazzBeanIdMap = {}

        # 初始化参数
        BeanManager.manager = self;

        # 注册组件
        self.batchRegister(self.formatBeanComponent())

        # 范围容器事件
        self.scopeEvent = {};

    @classmethod
    def getBeanManager(cls)->'BeanManager':

        return cls.manager

    # 创建容器管理对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def make(cls,components = {})->'BeanManager':

        return cls(components);


    def setScopeEvent(self,**scopeEvent):

        self.scopeEvent = scopeEvent;

        return ;
    # 创建容器管理对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def makeContainer(self,scope):

        return Container(scope);

    # 获取指定应用对应的容器对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param scope 应用级别
    def getScopeContainer(self,scope)->Container:

        scopeContainerFunc = self.scopeEvent.get(scope,None)

        if scopeContainerFunc is None:
            container = self.scopeContainer.get(scope,None);
            if container is None:
                container = Container(scope);
                self.scopeContainer[scope] = container
        else:
            container = scopeContainerFunc();

        return container

    # 清理容器
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def cleanScopeContainer(self,scopes = []):

        if scopes.count() == 0 :
            scopes.append(self.SCOPE_REQUEST)

        for scope in scopes:
            self.scopeContainer.pop(scope)


    # 获取bean 实例
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    # :param args 对象参数
    def getBean(self,beanId,*args ,**kwargs):

        definition = self.getDefinition(beanId)
        container = definition.getContainer()
        bean = None
        if container.hasBean(beanId) :
            bean = container.getBean(beanId)
        else:
            bean = definition.make([args,kwargs])
            if definition.isSingle():
                container.setBean(beanId,bean)

        return bean

    # 是否定义bean
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    # :param args 对象参数
    def hasComponent(self, beanId):

        component = self.components.get(beanId, None)
        if component is not None:
            return True
        else:
            return False

    # 创建一个新的bean对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    # :param args 对象参数
    def makeBean(self, beanId, *args ,**kwargs):

        definition = self.getDefinition(beanId)
        bean = definition.make([args,kwargs])

        return bean

    # 获取bean 定义对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    def getDefinition(self,beanId)->Definition:


        definition = self.definitions.get(beanId,None)
        if definition:
            return definition;

        component = self.components.get(beanId,None)
        if component is None:
            component = {self.CLASS_KEY_NAME: beanId}


        self.definitions[beanId] = Definition(**component)

        return self.definitions[beanId]

    # 批量注册bean组件
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    def batchRegister(self,components = {}):

        self.components.update(components)

    # 追加配置
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    # :param component bean 配置信息
    def appendComponent(self,beanId = '', component={}):

        return ;

    # 获取组件配置
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    def getComponents(self):

        return self.components

    # 注册装饰器bean 配置定义
    # <B> 说明： </B>
    # <pre>
    # 注入的属性自动叠加
    # </pre>
    @classmethod
    def registerBeanComponent(cls,clazz,bean):

        beanComponent = cls.clazzBeanComponents.pop(clazz,None)
        if beanComponent is None:
            beanComponent = bean
        else:
            beanComponent.update(bean)

        cls.clazzBeanComponents[clazz] = beanComponent;

        if cls.manager is not None:
            component = cls.formatComponentForBean(clazz,beanComponent)
            cls.manager.batchRegister(component);

        return ;


    @classmethod
    def formatComponentForBean(self,clazz,beanComponent):

        beanId = beanComponent.pop('id', None)
        if not beanId:
            beanId = clazz
        else:
            beanComponent['id'] = beanId;

        component = {};
        component[beanId] = beanComponent

        return component;

    @classmethod
    def formatBeanComponent(cls):

        componentList = {};
        for clazz in cls.clazzBeanComponents:
            beanComponent =  cls.clazzBeanComponents[clazz]
            beanId = beanComponent.pop('id',None)
            if not beanId:
                beanId = clazz
            else:
                beanComponent['id'] = beanId;

            componentList[beanId] = beanComponent

        return componentList
