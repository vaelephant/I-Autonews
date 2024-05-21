import requests
from bs4 import BeautifulSoup
import re
from .utils import save_to_file, extract_title, sanitize_filename

def load_url(url: str, jina_reader: bool):
    print("URL:", url)
    if jina_reader:
        try:
            print("Using Jina Reader to load URL")
            jina_url = f"https://r.jina.ai/{url}"
            response = requests.get(jina_url)
            response.raise_for_status()  # 检查HTTP请求是否成功
            data = response.text
            
            # 模拟从响应中解析Markdown内容
            if "automated queries" in data:
                content = (
                    "Title: Sorry...\n\n"
                    f"URL Source: {url}\n\n"
                    "Markdown Content:\n"
                    "We're sorry...\n"
                    "--------------\n\n"
                    "... but your computer or network may be sending automated queries. "
                    "To protect our users, we can't process your request right now.\n"
                )
            else:
                content = data

            title = extract_title(content, jina_reader)
            print("Title:", title)
            #不打印文章内容
            #print("Content:", content)

            # 将内容保存到文件
            sanitized_title = sanitize_filename(title)
            save_to_file(content, f'{sanitized_title}.txt')
            return {'Document': {'pageContent': content}}
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    else:
        try:
            print("Using BeautifulSoup to load URL")
            response = requests.get(url)
            response.raise_for_status()  # 检查HTTP请求是否成功
            soup = BeautifulSoup(response.content, 'html.parser')
            docs = soup.prettify()

            title = extract_title(response.content, jina_reader)
            print("Title:", title)
            #print("Content:", docs)

            # 将内容保存到文件
            sanitized_title = sanitize_filename(title)
            save_to_file(docs, f'{sanitized_title}.txt')
            return docs
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
