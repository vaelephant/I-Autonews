import requests

# 替换为你的钉钉 Webhook URL
DINGTALK_WEBHOOK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=425c68f64d086699fcc1082b8975a12ccc0a7978777717d48502f6e8738afcbf'

# 发送钉钉消息
def send_dingtalk_message(title, url, description, summary):
    message = f"### 新闻自动化 摘要\n\n"
    message += f"- **标题**: {title}\n"
    message += f"- **连接**: {url}\n"
    message += f"- **内容**: {description}\n"
    message += f"- **摘要**: {summary}\n"

    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "AutoNews 通知",
            "text": message
        }
    }

    try:
        response = requests.post(DINGTALK_WEBHOOK_URL, json=data)
        response.raise_for_status()
        print('Message sent to DingTalk:', response.json())
        print(message)
    except requests.exceptions.RequestException as e:
        print('Error sending message to DingTalk:', e)

# 模拟调用发送自动新闻摘要函数
# send_dingtalk_message(
#     "新闻示例",
#     "https://example.com/article",
#     "这是一篇示例文章的描述。",
#     "这是一篇示例文章的摘要。"
# )

send_dingtalk_message(
    "正在获取新闻标题",
    "正在获取新闻连接",
    "正在生成新闻内容",
    "正在生成新闻摘要"
)

