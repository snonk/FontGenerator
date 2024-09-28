from google.cloud import documentai_v1beta3 as documentai
from PIL import Image, ImageDraw, ImageOps, ImageFont

import os
# import pil_font_maker

img_path = "test/long.jpg"

def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document"s text. This function converts
    offsets to a string.
    """
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    return "".join(
        text[int(segment.start_index) : int(segment.end_index)]
        for segment in layout.text_anchor.text_segments
    )

def process_document(file_path):
    # Initialize Document AI client
    client = documentai.DocumentProcessorServiceClient()

    # Path to your processor (replace with your Document AI processor ID)
    processor_name = 'projects/365307119423/locations/us/processors/e761dbbe7172089f'

    # Read the file into memory
    with open(file_path, 'rb') as image_file:
        content = image_file.read()

    # Convert the file into a Document object
    raw_document = documentai.RawDocument(content=content, mime_type='image/jpeg')
    # image = cv2.imread(img_path)

    process_options = documentai.ProcessOptions(
        ocr_config=documentai.OcrConfig(
            enable_symbol=True,
        )
    )
    # Send document to the Document AI API
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document, process_options=process_options)
    response = client.process_document(request=request)

    # Extract the Document object from the response
    document = response.document
    text = document.text



    # Iterate through pages
    for page in document.pages:
        # Iterate through each paragraph, word, and symbol (character)
        for symbol in page.symbols:
            char = layout_to_text(symbol.layout, text)
            print("symbol: ", char)
            bounds = symbol.layout.bounding_poly.vertices
            # print(symbol.layout.bounding_poly.vertices[0].x)

            document_image = Image.open(img_path)
            draw = ImageDraw.Draw(document_image)
            
            # Draw the bounding box around the form_fields
            # First get the co-ords of the field name
            vertices = []
            for vertex in symbol.layout.bounding_poly.normalized_vertices:
                vertices.append({'x': vertex.x * document_image.size[0], 'y': vertex.y * document_image.size[1]})
            # draw.polygon([
            #         vertices[0]['x'], vertices[0]['y'],
            #         vertices[1]['x'], vertices[1]['y'],
            #         vertices[2]['x'], vertices[2]['y'],
            #         vertices[3]['x'], vertices[3]['y']], outline='red')
            cropped = document_image.crop((vertices[0]['x'], vertices[0]['y'], vertices[2]['x'], vertices[2]['y']))
            inverted = ImageOps.invert(cropped)
            
            inverted.save(f"out/char_{ord(char)}.png")
        
    ### generate space
    char = Image.open("out/char_101.png")
    space = Image.new("RGB",(char.size[0], char.size[1]))
    space.save("out/char_32.png")

    # process_document(img_path)
    os.system("pil-font-encode out/ file.pil")

def generate_image(font_path, text):

    img = Image.new("RGB", (1280, 500), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # use a bitmap font
    font = ImageFont.load(font_path)

    draw.text((10, 10), text, 'blue', font=font)

    img.save("out.png")

# if __name__ == "__main__":
    
