from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your actual API key
API_KEY = 'YOUR_API_KEY'
API_URL = 'https://v6.exchangerate-api.com/v6/{}/latest/{}'

def get_conversion_rate(from_currency, to_currency):
    url = API_URL.format(API_KEY, from_currency)
    response = requests.get(url)
    data = response.json()
    
    if 'rates' in data:
        rate = data['rates'].get(to_currency, 'Currency not found')
        return rate
    else:
        return 'Error fetching rates'

@app.route('/', methods=['GET', 'POST'])
def index():
    conversion_rate = None
    if request.method == 'POST':
        from_currency = request.form.get('from_currency').upper()
        to_currency = request.form.get('to_currency').upper()
        conversion_rate = get_conversion_rate(from_currency, to_currency)
    
    return render_template('index.html', conversion_rate=conversion_rate)

if __name__ == '__main__':
    app.run(debug=True)
