import requests
from groq import Groq

def generate_text_with_llm(prompt):
    """
    使用大语言模型生成文本。
    
    参数:
    prompt (str): 输入提示文本
    
    返回:
    str: 生成的文本
    """
    api_url = 'http://localhost:11434/api/generate'  # 本地 API URL
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'llama3',
        'prompt': prompt,
        'stream': False
    }
    response = requests.post(api_url, headers=headers, json=data)
    
    try:
        response.raise_for_status()  # 检查响应状态
       # print(response.status_code)
       
        result = response.json()  # 解析 JSON 数据
        #print(result)
        
        # 从结果中提取生成的文本
        return result['response']
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print(f"Response content: {response.content}")  # 打印响应内容
        raise
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        raise

# Groq 框架
def generate_text_with_groq(prompt):
    client = Groq(
    api_key="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"
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-70b-8192",
    )
    result = chat_completion.choices[0].message.content
    # print(chat_completion.choices[0].message.content)
    return result

if __name__ == "__main__":
    prompt = "1=+1=？，请用中文回答"
    try:
        generated_text = generate_text_with_llm(prompt)
        print(generated_text)
    except Exception as e:
        print(f"发生错误: {e}")
