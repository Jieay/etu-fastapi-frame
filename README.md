# 概括
    etu 系列（easy to use）
    让技术更容易使用！
    EFF脚手架工具(Etu FastAPI Frame)是在开源FastAPI框架的基础上封装而成，以更快捷简便的命令方式，快速创建项目工程，以方便开发使用。
    

## 说明
    本包名字为 etu-fastapi-frame , 它主要是EFF脚手架工具的封装。其中支持的FastAPI框架版本：0.95.2


### 打包方法
    1. 将要打包的代码文件，统一放在一个目录中，目录名就是pip包的名字；
    2. 在目录外创建一个setup.py文件，并配置好；
    3. 执行 python setup.py sdist命令，完成打包；
    4. 完成打包后，便可通过 pip install 命令进行安装。

### 安装方法
    通过pip命令进行安装：pip install etu-fastapi-frame==1.0.0
   

### 参数说明
```shell
usage: eff-admin label server project_name
labels:
    0.95.2
server:
    cfg
    ms
```


### 使用方法
```shell
cd ~
eff-admin 0.95.2 ms gaofeng-ms
```


### 错误反馈