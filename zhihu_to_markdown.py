import json
import os
import re

import click
import html2text
import requests
from bs4 import BeautifulSoup


@click.command()
@click.argument('article_number')
@click.option('--save_dir', default='.', help='markdown储存地址', show_default=True)
@click.option('--image_dir', default='media', help='图片储存地址', show_default=True)
def _zhihu2markdown(article_number, save_dir, image_dir):
    """
    将知乎专栏文章转成markdown格式, 存入`save_dir/title.md`, 若文章中有图片, 将其保存在`image_dir`
    article_number为知乎专栏文章的网址编号. 如：https://zhuanlan.zhihu.com/p/12345678，输入12345678
    """""
    zhihu2markdown(article_number, save_dir, image_dir)


def zhihu2markdown(article_number: str, save_dir: str = '.', image_dir: str = 'media') -> None:
    """
    将知乎专栏文章转成markdown格式, 存入`save_dir/title.md`, 若文章中有图片, 将其保存在`image_dir`
    
    :param article_number: 知乎专栏文章的网址编号（如：https://zhuanlan.zhihu.com/p/12345678，输入12345678)
    :param save_dir: markdown文件储存路径
    :param image_dir: (若有)图片储存路径
    """""
    url = r'https://api.zhihu.com/article/' + article_number
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
    res = requests.get(url, headers=header)
    json_data = json.loads(res.text)
    title = json_data['title']
    title = re.sub('[^\w\-_\. ]', '_', title)
    soup = BeautifulSoup(json_data['content'], features='lxml')

    images = soup.find_all('img')
    md_path = os.path.join(save_dir, f'{title}.md')
    if len(images) > 0:
        image_dir = os.path.join(save_dir, image_dir)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir, exist_ok=True)
        for img in images:
            image_file_name = img['src'].split('/')[-1]
            if 'equation' not in image_file_name:
                path = os.path.join(image_dir, image_file_name)
                relative_path = os.path.join('.', image_dir, image_file_name)
                res = requests.get(img['src'], headers=header)
                with open(path, 'wb') as img_file:
                    img_file.write(res.content)
                img.attrs.clear()
                img['src'] = relative_path
            else:
                tex_doc = img['alt']
                img.string = '$' + tex_doc + '$'
                img.name = 'span'
                img.attrs.clear()
                img['class'] = 'text/tex'

    simplified_html = str(soup)
    simplified_html = simplified_html.replace('<i>', '')
    simplified_html = simplified_html.replace('</i>', '')
    md = html2text.html2text(simplified_html, bodywidth=0)
    md = md.replace('left\\\\', 'left\\')
    md = md.replace('right\\\\', 'right\\')
    md = md.replace('$\\\\[', '$')
    md = md.replace('\\\\]$', '$')
    md = md.replace('![]', '![a]')
    md = title + '\n===\n' + md

    with open(md_path, 'w', encoding='utf-8') as markdown_file:
        markdown_file.write(md)


if __name__ == '__main__':
    _zhihu2markdown()
