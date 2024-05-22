import os
import json
import requests
from dotenv import load_dotenv
from termcolor import colored, cprint
from web_loader import load_url  # 确保这个模块存在并且能够正确导入
from llms.llm_operations import generate_text_with_llm  # 导入 LLM 操作模块
import dingding.notifier as notifier

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中读取 Google News API 密钥
api_key = os.getenv('GOOGLE_NEWS_API_KEY')

# 搜索关键词
search_keyword = "大模型"

# 采集新闻数量
number_of_articles = 1

def print_startup_message():
    """
    打印启动消息。
    """
    cprint("**************************************************", 'green')
    cprint("*                                                *", 'green')
    cprint("*       欢迎使用 AutoNews：采集+生成+应用        *", 'green', attrs=['bold'])
    cprint("*                                                *", 'green')
    cprint("**************************************************", 'green')
    cprint("Fetching the latest news articles...", 'cyan')

def fetch_news(api_key, search_keyword):
    """
    使用 Google News API 获取新闻文章。
    
    参数:
    api_key (str): Google News API 密钥
    search_keyword (str): 搜索关键词
    
    返回:
    list: 包含新闻文章的列表
    """
    try:
        # 发送HTTP请求到Google News API
        response = requests.get(f"https://newsapi.org/v2/everything?q={search_keyword}&apiKey={api_key}")
        response.raise_for_status()  # 如果请求失败，则引发HTTPError异常

        # 解析返回的JSON数据
        data = response.json()

        # 检查请求是否成功
        if data['status'] == 'ok':
            return data['articles'][:number_of_articles]  # 只读取前1篇文章
        else:
            print("Failed to retrieve news. Check your API key and source.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"HTTP请求错误: {e}")
        return []

def main():
    print_startup_message()
    print(f"\n\n搜索关键词: {search_keyword}")
    print(f"采集新闻数量: {number_of_articles}")
  
    articles = fetch_news(api_key, search_keyword)
    for i, article in enumerate(articles, 1):
        # 使用f-string格式化输出
        print(f"\n\n文章 {i}:")
        print(f"标题: {article['title']}")
        print(f"链接: {article['url']}")
        if 'description' in article:
            print(f"内容: {article['description']}")
        print("\n\n----------------------------------------")

        jina_reader = True
        result = load_url(article['url'], jina_reader)

        # 获取网页内容
        content = result['Document']['pageContent'] if 'Document' in result else result.get('error', 'No content')

        if content:
            # 调用 LLM 生成文本摘要
            print("\n\n----------开始生成摘要--------------")
            # summary = generate_text_with_llm(f"请生成中文模拟摘要:{content[:1000]}")  # 生成前1000字符的摘要示例
            summary = []
            # 输出摘要
            # print(f"\n\n 请生成中文模拟摘要: {summary}")

            # 发送钉钉消息通知
            notifier.send_dingtalk_message(article['title'], article['url'], article.get('description', ''), summary)
        else:
            print("无法获取文章内容。")

if __name__ == "__main__":
    main()
