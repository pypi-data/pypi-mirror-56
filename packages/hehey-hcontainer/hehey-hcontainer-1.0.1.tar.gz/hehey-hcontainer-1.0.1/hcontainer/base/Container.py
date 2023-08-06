# -*- coding: utf-8 -*-


"""
 * 容器类
 *<B>说明：</B>
 *<pre>
 *  略
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
class Container:

    # 构造器
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param scope 应用级别
    def __init__(self,scope):

        # 容器有效范围
        # <B> 说明： </B>
        # <pre>
        # app 应用级别，forever 永远不失效
        # </pre>
        self.scope = scope

        # bean 对象列表
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.beans = {}


    # bean是否存在
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    def hasBean(self,beanId = '')->bool:

        if self.beans.get(beanId,None) is None:
            return False
        else:
            return True


    # 获取 bean 对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param id bean id
    def getBean(self,beanId = ''):

        return self.beans.get(beanId,None)

    # 设置bean对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    # :param bean bean 对象
    def setBean(self,beanId,bean = object):

        self.beans[beanId] = bean

        return ;

