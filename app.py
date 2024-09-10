from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def get_conversion_rate(from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Error: API request failed with status code {response.status_code}")
    
    if not response.text.strip():
        raise Exception("Error: Received empty response from the API.")

    if 'application/json' in response.headers.get('Content-Type', ''):
        try:
            data = response.json()
        except ValueError:
            raise Exception(f"Error: Unable to parse JSON from response: {response.text}")
    else:
        raise Exception(f"Error: API returned non-JSON response: {response.text}")

    rate = data.get('rates', {}).get(to_currency)
    if rate is None:
        raise Exception(f"Error: Conversion rate for {to_currency} not found.")
    
    return rate

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    from_currency = request.form['from_currency']
    to_currency = request.form['to_currency']
    amount = float(request.form['amount'])

    try:
        rate = get_conversion_rate(from_currency, to_currency)
        converted_amount = amount * rate
        return jsonify({'converted_amount': converted_amount, 'rate': rate})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
