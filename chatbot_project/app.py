from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/process_response', methods=['POST', 'GET'])
def process_response():
    if request.method == "POST":
        user_message = request.get_json()['message']
        bot_message = 'did you really just say: ' + user_message + '??!!'
        return jsonify({'message': bot_message}), 200
    else:
        return "This route only accepts POST requests."

@app.route('/')
def home():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)
