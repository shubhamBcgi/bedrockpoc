from flask import Flask, render_template, url_for
import pandas as pd

app = Flask(__name__)

# Load data from Excel file
df = pd.read_excel('community.xlsx')

@app.route('/')
def index():
    return render_template('index.html', data=df.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)