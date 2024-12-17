import pytesseract
import re
import cv2 as cv

def extract_text(warped_img):
    _, thresh = cv.threshold(warped_img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    text = pytesseract.image_to_string(thresh, lang="deu")

    pattern = r'\b[a-zA-Z0-9]\b'

    text = re.sub(pattern, '', text)
    return re.sub(r'[-_]', '', text)

def remove_extra_blank_lines(text):
    lines = text.splitlines()
    result_lines = []
    blank_line_count = 0

    for line in lines:
        if line.strip() == '':
            blank_line_count += 1
        else:
            if blank_line_count > 1:
                result_lines.append('')  # Behalte nur eine Leerzeile
            blank_line_count = 0
            result_lines.append(line)
    
    # Falls der Text mit mehreren Leerzeilen endet, behalte nur eine
    if blank_line_count > 1:
        result_lines.append('')

    return '\n'.join(result_lines)