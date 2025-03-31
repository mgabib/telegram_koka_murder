from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"  # Здесь позже добавится HTML-страница с игрой

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Убедись, что порт совпадает с Render!