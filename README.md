# python-micro
使用go-micro的proxy创建的Python微服务
和官方示例的区别在于，这里没有使用第三方http服务框架，使用的是python3自带的http server

## 基于go-micro
在运行之前需要开启
```
micro proxy
micro api --namespace=go.micro.srv
```

## 运行
```
Usage: main.py [-h|--help] [--host,127.0.0.1] [-p|--port,5000] [--proxy,127.0.0.1:8081]
```

## 编写服务
在handler中只需要定义相应的class，所有静态方法都被加载到rpc服务中，即classname.staticmethd为微服务method



