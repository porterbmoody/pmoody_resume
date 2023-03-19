from flask import Flask, render_template

app = Flask(__name__)

@app.route('/process_response', methods=['POST'])
def process_response(response):
    print("response")
    return 'did you really just say:' + response + "??!!"

@app.route('/')
def home():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)
