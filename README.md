# zhihu_to_markdown: 将知乎专栏的文章转成 HTML 及 Markdown 格式

本 python 脚本可以将知乎专栏的文章转成 Markdown 格式并将文章中的图片一起储存在本地。

提供的功能有：
* 将知乎专栏的文章转成 Markdown 格式，并且将文章中的图片全部存储到本地
* 可以选择将文章中的 TeX 公式以 TeX 代码的形式加载到 Markdown 文档中

## python 包依赖
* bs4
* click
* html2text
* requests

## 使用方法

    zhihu_to_markdown.py --help
    
    Usage: zhihu_to_markdown.py [OPTIONS] ARTICLE_NUMBER

      将知乎专栏文章转成markdown格式, 存入`save_dir/title.md`, 若文章中有图片, 将其保存在`image_dir`
      article_number为知乎专栏文章的网址编号.
      如：https://zhuanlan.zhihu.com/p/12345678，输入12345678

    Options:
      --save_dir TEXT   markdown储存地址  [default: .]
      --image_dir TEXT  图片储存地址  [default: media]
      --help            Show this message and exit.
