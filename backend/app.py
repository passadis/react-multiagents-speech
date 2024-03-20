import os
import base64
from flask import Flask, request, jsonify
import azure.cognitiveservices.speech as speechsdk
import weather_service
import news_service
import stock_service
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.ERROR)

# Azure Speech Service configuration using environment variables
speech_key = os.getenv('SPEECH_KEY')
speech_region = os.getenv('SPEECH_REGION')
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)

# Set the voice name (optional, remove if you want to use the default voice)
speech_config.speech_synthesis_voice_name='en-US-JennyNeural'

def text_to_speech(text, voice_name='en-US-JennyNeural'):
    try:
        # Set the synthesis output format to MP3
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
        
        # Set the voice name dynamically
        speech_config.speech_synthesis_voice_name = voice_name

        # Create a synthesizer with no audio output (null output)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        result = synthesizer.speak_text_async(text).get()

        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
            return result.audio_data  # This is in MP3 format
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            print("Error details: {}".format(cancellation_details.error_details))
            return None
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        return None

@app.route('/talk-to-rita', methods=['POST'])
def talk_to_rita():
    try:
        # Use default coordinates or get them from request
        latitude = 37.98  # Default latitude
        longitude = 23.72  # Default longitude
        data = request.json
        if data:
            latitude = data.get('latitude', latitude)
            longitude = data.get('longitude', longitude)

        # Get weather description using the weather service
        descriptive_text = weather_service.get_weather_description(latitude, longitude)
        
        if descriptive_text:
            
            audio_content = text_to_speech(descriptive_text, 'en-US-JennyNeural')  # Use the US voice
            #audio_content = text_to_speech(descriptive_text)
            if audio_content:
                # Convert audio_content to base64 for JSON response
                audio_base64 = base64.b64encode(audio_content).decode('utf-8')
                return jsonify({"audioContent": audio_base64}), 200
            else:
                return jsonify({"error": "Failed to synthesize speech"}), 500
        else:
            return jsonify({"error": "Failed to get weather description"}), 500
    except Exception as e:
        # Log the detailed error message
        logging.error(f"Error in /your-route: {traceback.format_exc()}")
        # Return a generic error message to the user
        return jsonify({"error": "An internal error has occurred!"}), 500
        
@app.route('/talk-to-mark', methods=['POST'])
def talk_to_mark():
    try:
        gnews_api_key = os.getenv('GNEWS_API_KEY')
        news_headlines = news_service.fetch_greek_news(gnews_api_key)

        # Set the language to Greek for MARK
        # speech_config.speech_synthesis_voice_name = 'el-GR-AthinaNeural'  # Example Greek voice

        audio_content = text_to_speech(news_headlines, 'el-GR-NestorasNeural')  # Use the Greek voice

        if audio_content:
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')
            return jsonify({"audioContent": audio_base64}), 200
        else:
            return jsonify({"error": "Failed to synthesize speech"}), 500
    except Exception as e:
        # Log the detailed error message
        logging.error(f"Error in /your-route: {traceback.format_exc()}")
        # Return a generic error message to the user
        return jsonify({"error": "An internal error has occurred!"}), 500
        
@app.route('/talk-to-mary', methods=['POST'])
def talk_to_mary():
    try:
        data = request.json
        stock_symbol = data.get('symbol')  # Extract the stock symbol from the request

        if not stock_symbol:
            return jsonify({"error": "No stock symbol provided"}), 400

        api_key = os.getenv('ALPHAVANTAGE_API_KEY')  # Get your Alpha Vantage API key from the environment variable
        stock_info = stock_service.fetch_stock_quote(api_key, stock_symbol)

        audio_content = text_to_speech(stock_info, 'en-US-JennyNeural')  # Use an English voice for Mary
        if audio_content:
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')
            return jsonify({"audioContent": audio_base64}), 200
        else:
            return jsonify({"error": "Failed to synthesize speech"}), 500
    except Exception as e:
        print(f"Error in /talk-to-mary: {e}")
        return jsonify({"error": str(e)}), 500
        
if __name__ == '__main__':
    app.run(debug=False)
