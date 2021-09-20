## Requirements:

    brew install tesseract

    pip3 install pytesseract
    pip3 install opencv-python
    pip3 install pillow
    pip3 install imutils
    pip3 install numpy

## Setup python38 for Jupyter

brew install python38
/usr/local/Cellar/python\@3.8/3.8.12/bin/python3 -m pip install ipykernel
/usr/local/Cellar/python\@3.8/3.8.12/bin/python3 -m pip install pytesseract opencv-python imutils pillow imutils numpy
/usr/local/Cellar/python\@3.8/3.8.12/bin/python3 -m pip install matplotlib

### tesseract: Failed loading language \'terminus\'
cd /usr/local/Cellar/tesseract/4.1.1/share/tessdata
cp snum.traineddata terminus.traineddata

/usr/local/Cellar/python\@3.8/3.8.12/bin/python3 -m ipykernel install -name python38
export TESSDATA_PREFIX=/usr/local/Cellar/tesseract/4.1.1/share/tessdata/
jupyter notebook

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