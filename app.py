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
    """獲取天氣信息"""
    config = load_config()
    try:
        # 這裡需要替換成實際的天氣 API
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={config['city']}&appid={config['weather_api_key']}&units=metric")
        weather_data = response.json()
        return {
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description'],
            'humidity': weather_data['main']['humidity']
        }
    except Exception as e:
        return {'error': str(e)}

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
        response = requests.post('http://localhost:11434/api/generate', 
                               json={
                                   "model": "llama2",
                                   "prompt": f"請總結以下內容：\n{text}",
                                   "stream": False
                               })
        return response.json()['response']
    except Exception as e:
        return f"無法生成摘要: {str(e)}"

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
    