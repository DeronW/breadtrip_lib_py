Breadtrip lib py
================

# 改该项目不再维护, 请不要使用

项目代码已经很就旧了, 并且我已经不在面包旅行, 并不清楚内部开发框架的最新进展. 按照技术更新迭代来说, 改该项目已经不再不在使用

# 以前的用法是这样的
Breadtrip's python lib for everyone.

Please add this directory to your PYTHONPATH by add follow line to your .bashrc: ::

    export PYTHONPATH=$PYTHONPATH:[YOUR "breadtrip_lib_py" path]

    Or add a pth file in your site-packages directory.

# 现在的用法是这样的

#### 目的

整理breadtrip项目中使用到的通用python的库,通过pip管理自己的私有python库,安装\卸载\升级可以通过pip,减少手动安装的麻烦及版本管理的复杂度

#### 使用方法

安装前要先删除旧的环境变量设置,以免引起冲突

安装

    如果远程库为私有库:
    pip install -e git+git@github.com:delongw/breadtrip_lib_py.git@master#egg=breadtrip 
    如果远程库为公有库:
    pip install -e git+https://github.com:delongw/breadtrip_lib_py.git@master#egg=breadtrip

卸载

    pip uninstall breadtrip

升级

    pip install -e git+git@github.com:delongw/breadtrip_lib_py.git@{new_version}#egg=breadtrip

注意

- 此代码库为breadtrip私用库,不应公开,不应在代码库中添加任何与环境相关配置,与项目相关配置,及与其它功能相关的key等.
- 代码库中如果有依赖的库需要在setup.py文件中标识出来并指定版本
- breadtrip包含若干python库,每一个库都会呗加入到当前的python环境变量中 *谨慎使用*
- 当breadtrip需要更新时,应更新所有正式环境\开发环境的breadtrip版本, 正式环境更新python库后需要重新启动服务

用pip通过github安装代码时需要当前系统安装git并且拥有远程代码库的权限,如果代码库为公开库则可以通过https协议来安装, 例如:


#### 清除旧代码

使用pip安装的方式安装breadtrip后需要清除BreadTripServer项目中遗留的代码及配置以免引起冲突.

清除方法:

1. 如果修改 $PYTHONPATH ,只需要关掉当前shell,重新打开一个
2. 如果修改 .bashrc 文件,则要在.bashrc文件中删除有关配置,打开一个新的shell
3. 如果是添加到系统默认的site-packages 或 dist-package 中,则只要删除即可
4. 如果在breadtrip项目的settings*.py文件中添加了修改sys.path的设置,则需要注释掉这段设置: **sys.path.insert(0, 'path to breadtrip_lib_py')**

清除python的环境变量设置后, *BreadTripServer/breadtrip_lib_py* 路径下的库已经不会再被系统调用,删掉或保留均可

#### 参考资料
pip文档 [http://www.pip-installer.org/en/latest/logic.html#vcs-support](http://www.pip-installer.org/en/latest/logic.html#vcs-support)
