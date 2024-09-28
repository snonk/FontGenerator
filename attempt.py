from paddleocr import PaddleOCR, draw_ocr
import cv2
import matplotlib.pyplot as plt
import numpy as np

# Initialize the OCR engine
# ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Use English language model
ocr = PaddleOCR(
    det_model_dir='./inference/ch_ppocr_mobile_v2.0_det_infer',
    rec_model_dir='./inference/handwritten_rec_infer',
    use_angle_cls=True,
    lang='en'
)

# Read the image
img_path = 'test/sentence.png'
image = cv2.imread(img_path)

# Run the OCR engine to detect and recognize text
result = ocr.ocr(img_path, cls=True)

# Extract the bounding boxes and text results
for line in result:
    for word_info in line:
        bbox, text, confidence = word_info[0], word_info[1][0], word_info[1][1]
        print(f'Detected Text: {text}, Confidence: {confidence}')
        print(f'Bounding Box: {bbox}')
        
        # Draw the bounding box on the image
        cv2.polylines(image, [np.array(bbox, dtype=np.int32)], True, (0, 255, 0), 2)

# Save or display the resulting image with bounding boxes
cv2.imwrite("out.png", image)
# cv2.imshow('Detected Letters', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
