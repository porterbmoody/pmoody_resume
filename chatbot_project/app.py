from flask import Flask, request, jsonify, render_template
from SwagGPT import SwagGPT

app = Flask(__name__)

# init NLPModel
swag_model = SwagGPT()

@app.route('/process_response', methods=['POST', 'GET'])
def process_response():
    if request.method == "POST":
        user_response = request.get_json()['message']
        bot_message = swag_model.get_response(user_response)
        return jsonify({'message': bot_message}), 200
    else:
        return "This route only accepts POST requests."

@app.route("/refresh")
def refresh_chat():
    return render_template("chat.html")

@app.route('/')
def home():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)

# git add .
# git commit -m "chatgpt"
# git push