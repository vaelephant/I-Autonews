import requests
import psycopg2
from datetime import datetime

import requests
from bs4 import BeautifulSoup


# 配置
NEWS_API_KEY = '1a192ea753fd4c5d8a0201b4914158a2'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'
DATABASE_CONFIG = {
    'dbname': 'news_db',
    'user': 'your_db_user',
    'password': 'your_db_password',
    'host': 'localhost',
    'port': '5432'
}





# 获取新闻数据
def fetch_news():
    params = {
        'apiKey': NEWS_API_KEY,
        'country': 'us',
        'pageSize': 10
    }
    response = requests.get(NEWS_API_URL, params=params)
    return response.json()

#用RaderAPI 解析网页
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

            # 将内容保存到文件
            save_to_file(content, 'jina_reader_output.txt')
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

            # 将内容保存到文件
            save_to_file(docs, 'beautifulsoup_output.txt')
            print(f"Documents loaded and parsed from {url}:")
            print(docs)
            return docs
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

# 示例调用
url = "https://ollama.com/blog/llama-3-is-not-very-censored"
jina_reader = True
result = load_url(url, jina_reader)
print(result)


# 保存数据
def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# 保存新闻数据到数据库
def save_news_to_db(news_list):
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    
    for news in news_list:
        title = news['title']
        content = news['content']
        source = news['source']['name']
        url = news['url']
        published_at = datetime.strptime(news['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        
        cursor.execute("""
            INSERT INTO news (title, content, source, url, published_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, content, source, url, published_at))
    
    conn.commit()
    cursor.close()
    conn.close()

# 打印新闻标题和链接
def print_news(news_list):
    for news in news_list:
        title = news.get('title', 'No Title')
        url = news.get('url', 'No URL')
        content = news.get('content', 'No content')
        print(f"Title: {title}\nURL: {url}\n")

# 主函数
def main():
    news_data = fetch_news()
    if news_data.get('status') == 'ok':
        articles = news_data['articles']
        print_news(articles)
        #save_news_to_db(articles)
        print("Successfully fetched and saved news")
    else:
        print("Failed to fetch news")

if __name__ == "__main__":
    main()
