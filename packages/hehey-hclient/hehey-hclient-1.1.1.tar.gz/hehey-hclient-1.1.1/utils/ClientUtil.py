
import importlib

class ClientUtil:

    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def setAttrs(cls, object, attrDict={}):
        for attr in attrDict:
            setattr(object, attr, attrDict[attr])

    # 首字母大写
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def ucfirst(self, str):

        return str[0].upper() + str[1:]

    # 获取上一级路径
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def dirname(cls, clazz):

        packageClass = clazz.rsplit('.', 1)

        return packageClass[0];

    # 获取模块元素
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getModuleMeta(cls, module):

        if isinstance(module,str):
            packageModule = module.rsplit('.', 1)
            try:
                moduleMeta = importlib.import_module(packageModule[0])
            except Exception as e:
                raise e
            return getattr(moduleMeta, packageModule[1])
        else:
            return module

    # 构建类路径
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def buildClazzModule(cls, package,clazzName,suffix = ''):

        if suffix:
            className = ClientUtil.ucfirst(clazzName) + suffix
        else:
            className = ClientUtil.ucfirst(clazzName)

        return '{0}.{1}.{1}'.format(package,className,className)

    # 动态生成方法
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def buildAgentMethod(cls,obj,methodCodeStr,agentMethod):
        import types;

        methodCode = compile(methodCodeStr, '', 'exec')
        functionCode = [c for c in methodCode.co_consts if isinstance(c, types.CodeType)][0]
        func = types.FunctionType(functionCode, {})
        func = types.MethodType(func, obj)
        setattr(obj, agentMethod, func)

        return ;



