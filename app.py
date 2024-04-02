from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  
import numpy as np
import io, base64, torch, cv2
from PIL import Image
from io import BytesIO
app = Flask(__name__)
CORS(app)  # Allowing CORS for all routes

# Load YOLOv8 PyTorch model
from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.yaml") # build a new model from scratch
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)


# Label map to convert label numbers to text
# The label map for YOLOv5's pre-trained model on the COCO dataset contains 80 classes.
# Here is a dictionary that maps the label indices to their respective names.
label_map = {
    "0": "person",
    "1": "bicycle",
    "2": "car",
    "3": "motorcycle",
    "4": "airplane",
    "5": "bus",
    "6": "train",
    "7": "truck",
    "8": "boat",
    "9": "traffic light",
    "10": "fire hydrant",
    "11": "stop sign",
    "12": "parking meter",
    "13": "bench",
    "14": "bird",
    "15": "cat",
    "16": "dog",
    "17": "horse",
    "18": "sheep",
    "19": "cow",
    "20": "elephant",
    "21": "bear",
    "22": "zebra",
    "23": "giraffe",
    "24": "backpack",
    "25": "umbrella",
    "26": "handbag",
    "27": "tie",
    "28": "suitcase",
    "29": "frisbee",
    "30": "skis",
    "31": "snowboard",
    "32": "sports ball",
    "33": "kite",
    "34": "baseball bat",
    "35": "baseball glove",
    "36": "skateboard",
    "37": "surfboard",
    "38": "tennis racket",
    "39": "bottle",
    "40": "wine glass",
    "41": "cup",
    "42": "fork",
    "43": "knife",
    "44": "spoon",
    "45": "bowl",
    "46": "banana",
    "47": "apple",
    "48": "sandwich",
    "49": "orange",
    "50": "broccoli",
    "51": "carrot",
    "52": "hot dog",
    "53": "pizza",
    "54": "donut",
    "55": "cake",
    "56": "chair",
    "57": "couch",
    "58": "potted plant",
    "59": "bed",
    "60": "dining table",
    "61": "toilet",
    "62": "TV",
    "63": "laptop",
    "64": "mouse",
    "65": "remote",
    "66": "keyboard",
    "67": "cell phone",
    "68": "microwave",
    "69": "oven",
    "70": "toaster",
    "71": "sink",
    "72": "refrigerator",
    "73": "book",
    "74": "clock",
    "75": "vase",
    "76": "scissors",
    "77": "teddy bear",
    "78": "hair drier",
    "79": "toothbrush",
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    # Read binary data
    file_data = file.read()

    # Convert binary data to a PIL Image object
    image = Image.open(io.BytesIO(file_data))

    # Convert the PIL image to a numpy array
    image_np = np.array(image)
    
    # Convert the numpy array to a CV2 image
    img_cv2 = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Process the image
    results = model(img_cv2)
    
    if len(results) > 0:
        # Plot the annotated image
        annotated_image = results[0].plot()

        # Convert the annotated image from OpenCV format to PIL format
        annotated_image_pil = Image.fromarray(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))

        # Encode the image to bytes
        buffered = BytesIO()
        annotated_image_pil.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return jsonify({'image': 'data:image/png;base64,' + img_str})
    
    return jsonify({'error': 'No results from the model'})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5500,debug=True)



