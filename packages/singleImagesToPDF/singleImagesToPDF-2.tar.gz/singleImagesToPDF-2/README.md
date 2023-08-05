# singleImagesToPDF

This helps you to convert all the image files in your current working directory (os.getcwd()) to be combined in a PDF file format.

Supported File Formats :- JPEG/JPG/PNG
Supported Operating Systems :- Linux/Windows
Programming Language :- Python3

Using this you can convert all your images gathered (either notes or documents) to a single pdf file. 

All you need to do is:
    1) pip install single_images_to_pdf
    2) make a python script and add the following two lines of code
        a) Do the necessary import
            from pdf_from_multi_images import pdf_from_multi_imgs
        b) Make an instance and call the merge function
            a = pdf_from_multi_imgs()
            a.merge()

Follow along the instructions and your images (usually notes/documents) will be merged into a single pdf

Image Format supported :- JPG/JPEG/PNG

Platform Supported :- Linux/Windows
