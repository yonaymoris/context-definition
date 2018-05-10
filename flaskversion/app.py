from flask import Flask
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

# store positivity/negativity dictionary with add/edit/delete option
@app.route("/dictionary", methods=['GET', 'POST'])
def dictionary():
    return render_template('dictionary.html')

@app.route("/history", methods=['GET', 'POST'])
def history():
    return render_template('history.html')
