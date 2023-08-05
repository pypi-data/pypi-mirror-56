# encoding=utf-8
from distutils.core import setup
setup(
    name='xiaobo_test', # 对外我们模块的名字
    version='2.1', # 版本号
    description='这是第一个对外发布的模块，仅用作测试哦', #描述
    author='xiaobo', # 作者
    author_email='624737048@qq.com', py_modules=['pkg_c.test1','pkg_c.test2','pkg_c.test_import'] # 要发布的模块
)