from flask import Flask, request, send_file, jsonify
import soundfile as sf
from kokoro_onnx import Kokoro
import io

app = Flask(__name__)

kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request"}), 400

    text = data["text"]
    voice = data.get("voice", "af_heart")
    speed = float(data.get("speed", 1.0))
    lang = data.get("lang", "en-us") # lang can be 'en-us' or 'en-gb'

    samples, sample_rate = kokoro.create(text, voice=voice, speed=speed, lang=lang)
    buf = io.BytesIO()
    sf.write(buf, samples, sample_rate, format="WAV")
    buf.seek(0)
    return send_file(buf, mimetype="audio/wav", as_attachment=True, download_name="audio.wav")

if __name__ == "__main__":
    app.run(debug=True)