# 自己常用的代码封装了一下

## pip安装
```sh
pip3 install RookieTools
```

## 源码安装
> 源码安装我就测试了 Debian/Ubuntu操作系统  
> 其他系统未测试
```sh
# 项目依赖 requests and lxml

git clone https://github.com/hyll8882019/RookieTools.git
cd RookieTools
python3 setup.py build
python3 setup.py install
```

## 使用方法
```python
from RoookieTools.public.helper import get_md5
get_md5(123) # 返回md5值
```

[更新日志](CHANGELOG.md)