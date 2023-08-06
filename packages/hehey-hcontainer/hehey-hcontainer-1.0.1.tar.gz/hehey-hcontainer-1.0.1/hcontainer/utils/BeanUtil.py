# -*- coding: utf-8 -*-
import importlib,inspect,traceback
"""
 * 类帮助类
 *<B>说明：</B>
 *<pre>
 *  提供基本类操作,获取属性值,设置属性等等
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
class BeanUtil:

    BEAN_REF_REGEX = r'<ref::([^>]+)?>'
    PARAMS_REGEX = r'<(.+)::([^>]+)?>'

    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getAttrs(cls,object):
        attrs = dir(object);
        attrDict = {};
        for attr in attrs:
            if not attr.startswith("__"):
                attrDict[attr] = getattr(object,attr)

        return attrDict

    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def setAttrs(cls,object,attrDict = {}):
        for attr in attrDict:
            setattr(object, attr, attrDict[attr])

    def splitClassName(clazz):

        packageClass = clazz.rsplit('.', 1)

        return [packageClass[0],packageClass[1]]

    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getModuleMeta(cls,clazz):

        packageClass = clazz.rsplit('.', 1)
        packageMeta = importlib.import_module(packageClass[0])
        #
        return  getattr(packageMeta, packageClass[1])