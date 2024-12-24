import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 初始化数据库函数
def init_db():
    try:
        with sqlite3.connect('game.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception: {e}")

# 根路径视图函数
@app.route('/')
def index():
    # 获取得分历史记录
    with sqlite3.connect('game.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, score, date FROM players ORDER BY score DESC LIMIT 10")
        scores = cursor.fetchall()
    return render_template('index.html', scores=scores)  # 渲染 templates 目录下的 index.html

# 保存得分的路由
@app.route('/save_score', methods=['POST'])
def save_score():
    try:
        data = request.get_json()
        username = data.get('username')
        score = data.get('score')

        if not username or not score:
            return jsonify({"error": "Invalid data"}), 400

        with sqlite3.connect('game.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO players (username, score) VALUES (?, ?)", (username, score))
            conn.commit()

        return jsonify({"message": "Score saved successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

# 删除得分记录的路由
@app.route('/delete_score', methods=['POST'])
def delete_score():
    try:
        data = request.get_json()
        username = data.get('username')

        if not username:
            return jsonify({"error": "Invalid data"}), 400

        with sqlite3.connect('game.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM players WHERE username = ?", (username,))
            conn.commit()

        return jsonify({"message": "Score deleted successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    init_db()  # 调用初始化数据库函数
    app.run(debug=True)
