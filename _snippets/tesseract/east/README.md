already installed with opencv?

brew install tesseract --all-languages

tesseract-ocr, which is a great OCR library. If your documents have a fixed structured (consistent layout of text fields) then tesseract-ocr is all you need. For more advanced analysis checking out ocropus, which uses tesseract-ocr but adds layout analysis.

smell test   smoke test
tesseract -v

pip3 install pytesseract
pip3 install imutils

===

git clone https://github.com/argman/EAST.git

download east
https://drive.google.com/open?id=0B3APw5BZJ67ETHNPaU9xUkVoV0U
http://download.tensorflow.org/models/resnet_v1_50_2016_08_28.tar.gz

===

Ocular - Ocular works best on documents printed using a hand press, including those written in multiple languages. It operates using the command line. It is a state-of-the-art historical OCR system

? OCRopus - OCRopus is an open-source OCR system allowing easy evaluation and reuse of the OCR components by both researchers and companies. 
