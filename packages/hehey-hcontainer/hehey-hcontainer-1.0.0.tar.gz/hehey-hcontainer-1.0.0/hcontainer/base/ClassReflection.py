# -*- coding: utf-8 -*-
import inspect
from ..utils.BeanUtil import BeanUtil
import re
"""
 * bean 反射器
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
class ClassReflection:

    BEAN_REF_REGEX = r'<ref::([^>]+)?>'
    PARAMS_REGEX = r'<(.+)::([^>]+)?>'
    PARAMS_SPLIT_CHARACTER = '|';

    ARGS_DICT_ALIAS = '-**-';

    # 构造器
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param clazz 目标类名
    def __init__(self,clazz):

        # 目标类
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.clazz = clazz

        # 目标类的构造参数
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.parameters = {}

        # 构造器默认参数
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.defaultArgsDict = {}

        # 构造器默认参数序号index
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.defaultArgsIndexMap = []


    # 创建对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param clazz 目标类名
    def make(self,args):
        beanClazzMeta = BeanUtil.getModuleMeta(self.clazz)
        params = self.buildParmas(args);
        beanArgs = params[0];
        beankwArgs = params[1];

        return  beanClazzMeta(*beanArgs,**beankwArgs)


    # 合并构造参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param args 外部构造参数
    # :param params 默认构造参数
    def mergeArgs(self, beanArgs = [],defaultArgs = {}):

        from .Definition import Definition

        indexArgs = beanArgs[0]
        dictArgs = beanArgs[1]
        if not dictArgs:
            dictArgs = {};



        newDictArgs = {}
        newDictArgs.update(defaultArgs)
        newDictArgs.update(dictArgs)

        kwArgs = [];

        if indexArgs:
            for index in range(len(indexArgs)):
                name = self.defaultArgsIndexMap[index]
                if newDictArgs[name] == self.__class__.ARGS_DICT_ALIAS:
                    newDictArgs.update(indexArgs[index])
                else:
                    kwArgs.append(indexArgs[index]);
                newDictArgs.pop(name)

        clazzDictArgs = {};
        if newDictArgs:
            for name in newDictArgs:
                if newDictArgs[name] == self.__class__.ARGS_DICT_ALIAS:
                    continue;

                defaultValue = newDictArgs[name]
                if isinstance(defaultValue,Definition):
                    clazzDictArgs[name] = defaultValue.make([])
                else:
                    clazzDictArgs[name] = defaultValue


        return [kwArgs,clazzDictArgs]



    # 获取构造方法参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getDefaultArgs(self):

        if self.defaultArgsDict:
            return self.defaultArgsDict

        beanClassMeta = BeanUtil.getModuleMeta(self.clazz)

        signature = inspect.signature(beanClassMeta)
        defaultArgs = signature.parameters;

        for name, value in defaultArgs.items():

            if isinstance(value.default,str):
                self.defaultArgsDict[name] = self.getDefaultValue(value.default)
            elif str(value).find("**") != -1:
                self.defaultArgsDict[name] = self.__class__.ARGS_DICT_ALIAS
            else:
                self.defaultArgsDict[name] = value.default

            self.defaultArgsIndexMap.append(name)


        return self.defaultArgsDict

    # 构建真实默认构造参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def buildParmas(self,args = []):

        args = self.mergeArgs(args,self.getDefaultArgs())

        return args

    @classmethod
    def getDefaultValue(cls, value):

        from .Definition import Definition
        refMatch = re.match(cls.BEAN_REF_REGEX, value)
        if refMatch:
            ref = refMatch.group(1);
            definition = Definition(_ref = ref)
            value = definition
        else:
            funcMatch = re.match(cls.PARAMS_REGEX, value)
            if funcMatch:
                funcName = funcMatch.group(1);
                funcParams = funcMatch.group(2)
                funcMeta = BeanUtil.getModuleMeta(funcName)
                funcParamstuple = tuple(funcParams.split(cls.PARAMS_SPLIT_CHARACTER))
                definition = Definition(_func = [funcMeta,funcParamstuple])
                value = definition

        return value




