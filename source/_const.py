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
#豌豆荚存放文件夹路径
const.WANDOUJIA_DIR ="../file/"
#豌豆荚目录分类的Json文件路径
const.WANDOUJIA_CATA_JSON_FILE = const.WANDOUJIA_DIR+"wandoujia_file.json"
#豌豆荚app目录信息Json文件路径
const.WANDOUJIA_APPS_JSON_FILE = const.WANDOUJIA_DIR+"apps_file.json"
#豌豆荚app评论信息文件夹路径
const.WANDOUJIA_APPS_COMMENT_DIR = const.WANDOUJIA_DIR+"apps_comments/"
#豌豆加app详细的描述信息文件夹路径
const.WANDOUJIA_APPS_DESC_DIR = const.WANDOUJIA_DIR+"apps_detail_descripe/"

'''豌豆荚测试使用'''
#豌豆荚旅游出行URL
const.WANDOUJIA_CARA_TRIP_URL = "http://www.wandoujia.com/category/408"
