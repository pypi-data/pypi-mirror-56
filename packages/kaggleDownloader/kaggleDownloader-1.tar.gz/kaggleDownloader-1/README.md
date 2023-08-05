# kaggleDownloader

This helps you to download your Kaggle Dataset to your Google Colab Notebook by using<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;1) kaggle.json<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;2) Kaggle Dataset Download API link<br/>


Requirements:
======
File Required :- kaggle.json (obtain it from your kaggle account. Go to Kaggle.com -> Profile Pic -> My Account -> API -> Create New API Token) <br/>
Supported Platform :- Google Colab<br/>
Programming Language :- Python3<br/>

Using this you can download the Kaggle Dataset to your Google Colab Notebook.

How to Use?
======
All you need to do is open your google colab notebook and run:<br/>
    1) **!pip install singleImagesToPDF**<br/>
    2) make a python script and add the following lines of code<br/>
       &nbsp;&nbsp;&nbsp;&nbsp;a) Do the necessary **import**:-<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **from singleImagesToPDF.pdfFromMultiImages import pdfFromMultiImgs**<br/>
       &nbsp;&nbsp;&nbsp;&nbsp; b) After importing, Call 'get_dataset()' function<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**get_dataset()**<br/>

Follow along the instructions and you will be ready with your dataset to work with on your Colab Notebook.
