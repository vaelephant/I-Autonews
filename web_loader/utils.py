import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

def save_to_file(content, filename):
    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')
    # 创建以日期命名的文件夹
    if not os.path.exists(current_date):
        os.makedirs(current_date)
    # 创建完整的文件路径
    file_path = os.path.join(current_date, filename)
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
        print(f"\n \n采集内容  -- 《{file_path} 》-- 保存成功")

def extract_title(content, jina_reader):
    if jina_reader:
        # 模拟从Jina Reader响应中解析标题
        title_line = content.splitlines()[0]
        if title_line.startswith("Title: "):
            return title_line[7:]  # 提取标题
        return "No title found"
    else:
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        return title

def sanitize_filename(filename):
    # 去掉不合法的文件名字符
    return re.sub(r'[\\/*?:"<>|]', "", filename)
