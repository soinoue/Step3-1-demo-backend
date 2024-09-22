from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import os
# from dotenv import load_dotenv

# # .envファイルから環境変数を読み込む
# load_dotenv()

app = Flask(__name__)
CORS(
    app, 
    # resources={r"/api/*": {"origins": "http://localhost:3000"}}
    )  # CORS設定を更新

# OpenAI APIキーを環境変数から取得
openai.api_key = os.getenv("OPENAI_API_KEY")



# APIキーが正しく読み込まれているか確認（デバッグ用）
print("OpenAI API Key:", openai.api_key)


@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Flask start!'})

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify(message='Hello World by Flask')

@app.route('/api/multiply/<int:id>', methods=['GET'])
def multiply(id):
    print("multiply")
    # idの2倍の数を計算
    doubled_value = id * 2
    return jsonify({"doubled_value": doubled_value})

@app.route('/api/echo', methods=['POST'])
def echo():
    print("echo")
    data = request.get_json()  # JSONデータを取得
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    # 'message' プロパティが含まれていることを確認
    message = data.get('message', 'No message provided')
    return jsonify({"message": f"echo: {message}"})

@app.route('/api/gpt', methods=['POST'])
def gpt():
    print("gpt")
    # リクエストからプロンプトを取得
    data = request.get_json()
    print("Received data:", data)
    # prompt = data.get('message')
    # print(prompt)

    if data is None or 'prompt' not in data:
        print("Prompt is missing")  # プロンプトが欠如している場合
        return jsonify({"error": "Prompt is required"}), 400
    
    prompt = data['prompt']

    try:
        # OpenAI APIを使用してテキストを生成
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        # 生成されたテキストを返す
        generated_text = response['choices'][0]['message']['content'].strip()
        print(generated_text)
        return jsonify({"generated_text": generated_text})

    except Exception as e:
        print(f"Error: {str(e)}")  # エラーをターミナルに出力
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
