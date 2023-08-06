"""
作者：陈苏奕
更新时间：2019-11-29
说明：此库依赖于pymongo
"""
import pymongo


class ConnectMongo(object):

    def __init__(self, mongo_info):
        """
        :param mongo_info:
        传入的mongo_info必须是个字典
        其必须包含以下key
        mongo_uri
        mongo_db
        mongo_coll
        可以不包含的key如下
        user
        passwd
        source
        """
        # 此处定义了需要更新的表的信息
        self.mongo_uri = mongo_info['mongo_uri']
        self.mongo_db = mongo_info['mongo_db']
        self.mongo_coll = mongo_info['mongo_coll']
        if 'user' in mongo_info.keys():
            self.mongo_user = mongo_info['user']
            self.mongo_passwd = mongo_info['passwd']
            self.mongo_source = mongo_info['source']
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        try:
            self.db.authenticate(name=self.mongo_user, password=self.mongo_passwd, source=self.mongo_source)
        except (NameError, AttributeError):
            pass

    # 建立连接，返回游标，没有self.coll这个属性
    @property
    def get_coll(self):
        coll = self.db[self.mongo_coll]
        return coll

    def close_mongo(self):
        self.client.close()
