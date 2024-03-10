from flask import Flask, render_template, request, jsonify
import requests
import openai

app = Flask(__name__)
openai.api_key = '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'

def show_earnings(symbol):
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey=M6MP1BDPRRJJ7Q18"
    r = requests.get(url)
    data = r.json()
    return data

def analyze_earnings(symbol):
    earnings_data = show_earnings(symbol.upper())
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "Analyze this stocks earnings data if its a smart investment."}, {"role": "user", "content": str(earnings_data)}], max_tokens=400)
    return response['choices'][0]['message']['content'].strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    symbol = request.form['symbol']
    analysis_type = request.form['analysis']

    if analysis_type == 'earnings':
        result = analyze_earnings(symbol)
    # Add more conditions for other analysis types if needed

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
