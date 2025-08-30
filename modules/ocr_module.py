# OCR functions here
import pytesseract
from PIL import Image
import re

# Set tesseract cmd path for Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image: Image.Image) -> str:
    text = pytesseract.image_to_string(image)
    return text

def parse_inventory(text: str):
    """
    Parse text and return list of tuples: (item_name, quantity, expiry_date)
    Example: [('Milk', 1, '2025-09-05')]
    """
    items = []
    lines = text.split("\n")
    for line in lines:
        # Simple regex example to extract quantity and expiry (dd-mm-yyyy)
        match = re.search(r"(\w+)\s+(\d+)\s+(\d{2}[-/]\d{2}[-/]\d{4})", line)
        if match:
            item, qty, expiry = match.groups()
            # Normalize expiry format
            expiry = expiry.replace("/", "-")
            items.append((item, int(qty), expiry))
    return items
