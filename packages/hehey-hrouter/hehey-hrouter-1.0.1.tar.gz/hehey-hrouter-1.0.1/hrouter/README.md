# hehey-hrouter

#### 介绍
hehey-hrouter 是一个python 路由工具组件,仿Yii2 路由规则

#### 依赖以及版本要求
- python >= 3.5

#### 安装
- 直接下载:
```

```
- 命令安装：
```
pip install hehey-hrouter
```
#### 基础文件以目录


#### 参数配置


#### 基本示例
- 快速使用
```python
from hrouter.route import RouterManager
conf =  {
    'customRouter':{
        'clazz': 'easy',
        'rules':[],
        'actionRule':{
            'filter': ['site', 'controllers', 'modules'],
            'suffix': ['Action', 'Controller'],
            'func':''#action 地址处理方法
        }
    }
}

routerManager = RouterManager(**conf);
# 解析请求
routerRequest = routerManager.runRoute({'PATH_INFO':"news/list"});
routeUrl = routerRequest.getRouteUrl() # 获取路由解析后url地址,比如news/index
routeParams = routerRequest.getRouteParams();# 获取路由的解析后参数{"id":1}
# 生成url 地址
url = routerManager.buildUrl('news/detail',{"id":"10"})  
# url: news/detail?id=10

```

- 解析web请求地址
```python
# 浏览器输入:http://xxx.cn/news/index?id=1

from hrouter.route import RouterManager
conf =  {
    'customRouter':{
        'clazz': 'easy',
        'rules':[],
        'actionRule':{
            'filter': ['site', 'controllers', 'modules'],
            'suffix': ['Action', 'Controller'],
            'func':''#action 地址处理方法
        }
    },
    'routerRequest':"WebRouterRequest",# 默认为web 请求
}

routerManager = RouterManager(**conf);
# 解析请求
environ = {};# uwsgi environ 上下文
routerRequest = routerManager.runRoute(environ);
routeUrl = routerRequest.getRouteUrl() # 获取路由解析后url地址,比如news/index
routeParams = routerRequest.getRouteParams();# 获取路由的解析后参数{"id":1}

```

- 解析命令行请求地址
```python

# 控制台输入: python3 main.py news/detail?id=2

from hrouter.route import RouterManager
conf =  {
    'customRouter':{
        'clazz': 'easy',
        'rules':[],
        'actionRule':{
            'filter': ['site', 'controllers', 'modules'],
            'suffix': ['Action', 'Controller'],
            'func':''#action 地址处理方法
        }
    },
    'routerRequest':"ConsoleRouterRequest",
}

routerManager = RouterManager(**conf);
# 解析请求
environ = {};# uwsgi environ 上下文
routerRequest = routerManager.runRoute(environ);
routeUrl = routerRequest.getRouteUrl() # 获取路由解析后url地址,比如news/detail
routeParams = routerRequest.getRouteParams();# 获取路由的解析后参数{"id":2}

```


- 规则路由
```python
from hrouter.route import RouterManager
conf =  {
    'customRouter':{
        'clazz': 'easy',
        'rules':[
            # uri 请求地址规则,action 操作地址规则,method 请求方法,clazz 规则类,用于扩展
            #{'uri':'<news:\w+>/<id:\d+>','action':'<news>/index','method'='get','clazz'=>''},
            #{'uri':'<controller:\w+>/<action:\w+>','action':'<controller>/<action>'},

            {'uri':'<news:\w+>/<id:\d+>.html','action':'<news>/detail'}
        
        ],
        'actionRule':{
            'filter': ['site', 'controllers', 'modules'],
            'suffix': ['Action', 'Controller'],
            'func':''#action 地址处理方法
        }
    }
}

routerManager = RouterManager(**conf);
url = routerManager.buildUrl('news/detail',{"id":"10"})  
# url:news/detail?id=10

```


- 生成地址
```python
from hrouter.route import RouterManager
conf =  {
    'customRouter':{
        'clazz': 'easy',
        'rules':[
            # uri 请求地址规则,action 操作地址规则,method 请求方法,clazz 规则类,用于扩展
            #{'uri':'<news:\w+>/<id:\d+>','action':'<news>/index','method'='get','clazz'=>''},
            #{'uri':'<controller:\w+>/<action:\w+>','action':'<controller>/<action>'},

            {'uri':'<news:\w+>/<id:\d+>.html','action':'<news>/detail'}
        
        ],
        'actionRule':{
            'filter': ['site', 'controllers', 'modules'],
            'suffix': ['Action', 'Controller'],
            'func':''#action 地址处理方法
        }
    }
}

routerManager = RouterManager(**conf);
url = routerManager.buildUrl('news/detail',{"id":"10"})  
# url:news/detail?id=10

```

- 装饰器注册路由规则
```python
from hrouter.route import RouterManager,reg_route_rule
conf =  {
    'customRouter':{
        'clazz': 'easy',
        'rules':[
            # uri 请求地址规则,action 操作地址规则,method 请求方法,clazz 规则类,用于扩展
            #{'uri':'<news:\w+>/<id:\d+>','action':'<news>/index','method'='get','clazz'=>''},
            #{'uri':'<controller:\w+>/<action:\w+>','action':'<controller>/<action>'},

            {'uri':'<news:\w+>/<id:\d+>.html','action':'<news>/detail'}
        
        ],
        'actionRule':{
            'filter': ['site', 'controllers', 'modules'],
            'suffix': ['Action', 'Controller'],
            'func':''#action 地址处理方法
        }
    }
}

routerManager = RouterManager(**conf);

# 注册路由规则-函数
@reg_route_rule('getuser')
def getuser(self):

    print("pass")

    return "<h1>您好</h1>"

# 注册路由规则-类方法
class NewsController:

    @reg_route_rule('news/list',method = 'post')
    def index(self):

        return "<h1>您好</h1>"

    # 资讯详情
    def detail(self):

        return "<h1>您好</h1>"

# 创建路由request 对象
routerRequest = routerManager.runRoute({'PATH_INFO':"news/list"});
# 获取解析后的路由地址
routeUrl = routerRequest.getRouteUrl() # 获取路由解析后url地址,比如news/index
routeParams = routerRequest.getRouteParams();# 获取路由的解析后参数{"id":1}
# route = news/getindex

# 生成地址
url = routerManager.buildUrl('news/getuser',{"id":"10"})
# url: news/getuser?id=10
url = routerManager.buildUrl('getuser',{"id":"10"})
# url: getuser?id=10
url = routerManager.buildUrl('news/detail',{"id":"10"})
# url: news/10.html

url = routerManager.buildUrl('account/user/add',{"id":"10"})
# url: account/user/add?id=10



```