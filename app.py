from flask import Flask, render_template, request, Response, jsonify
import base64
from PIL import Image, ImageOps
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    try:
        frame_data = request.form['frame_data']
        # Decode the base64 frame data
        frame = base64.b64decode(frame_data.split(',')[1])
        # Convert to a PIL Image
        pil_image = Image.open(BytesIO(frame))

        # No color inversion, return the original frame
        buffer = BytesIO()
        pil_image.save(buffer, format="JPEG")
        original_frame_data = 'data:image/jpeg;base64,' + base64.b64encode(buffer.getvalue()).decode('utf-8')

        return jsonify({'original_frame_data': original_frame_data})
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing the frame.'})

if __name__ == "__main__":
    app.run(debug=True)
