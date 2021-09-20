## Requirements:

    brew install tesseract

    pip3 install pytesseract
    pip3 install opencv-python
    pip3 install pillow
    pip3 install imutils
    pip3 install numpy

### Links:

Hints

    fix DPI (if needed) 300 DPI is minimum
    fix text size (e.g. 12 pt should be ok)
    try to fix text lines (deskew and dewarp text)
    try to fix illumination of image (e.g. no dark part of image)
    binarize and de-noise image

preprocessing with cv2 https://nanonets.com/blog/ocr-with-tesseract/
+ Getting boxes around text
+ Blacklisting characters

training https://github.com/tesseract-ocr/tesseract/issues/2382