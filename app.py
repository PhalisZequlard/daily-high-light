from flask import Flask, render_template, jsonify, request
from datetime import datetime
import json
import requests
import pytz
import os

app = Flask(__name__)

# 配置文件路徑
CONFIG_PATH = 'config.json'
DATA_PATH = 'data.json'

def load_config():
    """載入配置文件"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_data():
    """載入數據文件"""
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tasks": [], "habits": [], "reminders": [], "schedule": []}

def save_data(data):
    """保存數據到文件"""
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_weather():
    """獲取天氣信息（使用 weatherapi.com 的免費 API）"""
    config = load_config()
    try:
        # 使用 weatherapi.com 的免費 API
        response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={config['weather_api_key']}&q={config['city']}&aqi=no")
        weather_data = response.json()
        return {
            'temperature': weather_data['current']['temp_c'],
            'description': weather_data['current']['condition']['text'],
            'humidity': weather_data['current']['humidity']
        }
    except Exception as e:
        # 如果 API 調用失敗，返回模擬數據
        return {
            'temperature': 25,
            'description': '晴天',
            'humidity': 60
        }

def get_daily_quote():
    """獲取每日一句"""
    try:
        response = requests.get("https://api.quotable.io/random")
        quote = response.json()
        return quote['content']
    except Exception:
        return "每一天都是新的開始！"

def get_ollama_summary(text):
    """使用 Ollama API 生成摘要"""
    try:
        # 添加更詳細的提示和錯誤處理
        prompt = """請根據以下資訊生成一個簡潔的每日總結：
        
        {text}
        
        請包含以下幾點：
        1. 今天最重要的事項
        2. 需要特別注意的提醒
        3. 建議與鼓勵
        
        請用溫暖積極的語氣撰寫。
        """
        
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "llama2",
                "prompt": prompt.format(text=text),
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            },
            timeout=30  # 添加超時設置
        )
        
        if response.status_code == 200:
            return response.json()['response']
        else:
            return "無法連接到 Ollama 服務，請確保服務正在運行。"
            
    except requests.exceptions.ConnectionError:
        return "無法連接到 Ollama 服務，請確保 Ollama 已經啟動並在運行。"
    except requests.exceptions.Timeout:
        return "請求超時，請稍後再試。"
    except Exception as e:
        return f"生成摘要時發生錯誤: {str(e)}\n請確保 Ollama 服務正常運行，並已安裝 llama2 模型。"

@app.route('/')
def index():
    """主頁面路由"""
    data = load_data()
    current_time = datetime.now(pytz.timezone('Asia/Taipei'))
    
    context = {
        'date': current_time.strftime('%Y年%m月%d日'),
        'time': current_time.strftime('%H:%M'),
        'weather': get_weather(),
        'schedule': data['schedule'],
        'tasks': data['tasks'],
        'habits': data['habits'],
        'reminders': data['reminders'],
        'quote': get_daily_quote()
    }
    
    return render_template('index.html', **context)

@app.route('/api/summary', methods=['POST'])
def generate_summary():
    """生成每日摘要"""
    data = load_data()
    summary_text = f"""
    今日行程：{', '.join(data['schedule'])}
    待辦事項：{', '.join(task['title'] for task in data['tasks'])}
    習慣追蹤：{', '.join(habit['name'] for habit in data['habits'])}
    提醒事項：{', '.join(data['reminders'])}
    """
    summary = get_ollama_summary(summary_text)
    return jsonify({'summary': summary})

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """添加待辦事項"""
    data = load_data()
    task = request.json
    data['tasks'].append(task)
    save_data(data)
    return jsonify({'status': 'success'})

@app.route('/api/habits', methods=['POST'])
def update_habit():
    """更新習慣追蹤"""
    data = load_data()
    habit = request.json
    data['habits'].append(habit)
    save_data(data)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)