from flask import Flask, request, render_template
import parse

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/results')
def result():
    return render_template('res.html', result=str(main_post()))

@app.route('/', methods=['POST'])
def main_post():
    text = request.form['text']
    return parse.run_treep(text)

if __name__ == '__main__':
    app.run(debug=True)
