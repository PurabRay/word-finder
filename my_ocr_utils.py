# from PIL import Image
# import pytesseract

# def extract_word_boxes(image_file):
#     """
#     Extract words and bounding boxes from an image file.
#     Returns a PIL image and a list of dictionaries containing:
#     - id: unique index
#     - text: recognized word
#     - left, top, width, height: OCR coordinates (top-left origin)
#     """
#     image = Image.open(image_file)
#     data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
#     boxes = []
#     for i in range(len(data['text'])):
#         if data['text'][i].strip():
#             boxes.append({
#                 'id': i,
#                 'text': data['text'][i],
#                 'left': data['left'][i],
#                 'top': data['top'][i],
#                 'width': data['width'][i],
#                 'height': data['height'][i]
#             })
#     return image, boxes
from PIL import Image
import pytesseract

def extract_word_boxes(image_file):
    """
    Extract words and bounding boxes from an image file.
    Returns a PIL image and a list of dictionaries containing:
      - id: unique index
      - text: recognized word
      - left, top, width, height: OCR coordinates (top-left origin)
      - line_num and block_num (if available)
    """
    image = Image.open(image_file)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    boxes = []
    for i in range(len(data['text'])):
        if data['text'][i].strip():
            box = {
                'id': i,
                'text': data['text'][i],
                'left': data['left'][i],
                'top': data['top'][i],
                'width': data['width'][i],
                'height': data['height'][i]
            }
            if 'line_num' in data:
                box['line_num'] = data['line_num'][i]
            if 'block_num' in data:
                box['block_num'] = data['block_num'][i]
            boxes.append(box)
    return image, boxes
