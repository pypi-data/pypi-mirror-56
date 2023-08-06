# Glimpse sdk

**服务接口sdk**

## 推送到pipy.org
##### 1.编辑setup.py，修改版本号

##### 2.创建~/.pypirc文件

    [distutils]
    index-servers=pypi
    
    [pypi]
    repository = https://upload.pypi.org/legacy/
    username = nilinside

##### 3.编译并上传代码到pipy.org
    #编译
    python setup.py build
    #打包
    python setup.py sdist
    #上传
    python setup.py sdist upload 
