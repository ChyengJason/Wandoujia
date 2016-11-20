#coding:utf-8
#常量池
class _const:
    class ConstError( TypeError ): pass
    class ConstCaseError( ConstError ): pass

    def __setattr__( self, name, value ):
        if name in self.__dict__:
            raise self.ConstError( "can't change const %s" % name )
        if not name.isupper():
            raise self.ConstCaseError( 'const name "%s" is not all uppercase' % name )
        self.__dict__[name] = value

const = _const()
#豌豆荚目录分类的URL
const.WANDOUJIA_CATA_URL = "http://www.wandoujia.com/category/app"
#豌豆荚目录分类的Json文件路径
const.WANDOUJIA_CATA_JSON_FILE = "../file/wandoujia_file.json"