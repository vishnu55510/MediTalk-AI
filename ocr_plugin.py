# File: ocr_extraction_plugin.py

import pytesseract
from PIL import Image
import os
from semantic_kernel.functions.kernel_function_decorator import kernel_function
class OCRExtractionPlugin:
    @kernel_function(name="extract_text", description="Extract text from an image")
    def extract_text(self, image_path: str) -> str:
        try:
            if not os.path.exists(image_path):
                return "❌ Error: File not found."

            image = Image.open(image_path)
            extracted_text = pytesseract.image_to_string(image)
            
            if not extracted_text.strip():
                return "⚠️ No text detected in the image."

            return extracted_text
        
        except Exception as e:
            return f"❌ Error extracting text: {str(e)}"
