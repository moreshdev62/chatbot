from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__, static_folder='templates', static_url_path='')
CORS(app)

# Инициализация Groq клиента
# API ключ берется из переменных окружения Render
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY", "")
)

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'reply': 'Пожалуйста, введите сообщение'}), 400
        
        # Проверка наличия API ключа
        if not client.api_key:
            return jsonify({'reply': 'Ошибка: API ключ Groq не настроен'}), 500
        
        # Запрос к Groq API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # или другую модель Groq
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        reply = completion.choices[0].message.content
        return jsonify({'reply': reply})
        
    except Exception as e:
        print(f"Ошибка: {e}")  # Логирование ошибки
        return jsonify({'reply': f'Извините, произошла ошибка. Попробуйте позже.'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
