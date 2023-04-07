import webbrowser
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    url = 'http://127.0.0.1:5000/'
    # webbrowser.open(url)
    app.run()


# git add .
# git commit -m "solar ai"
# git push