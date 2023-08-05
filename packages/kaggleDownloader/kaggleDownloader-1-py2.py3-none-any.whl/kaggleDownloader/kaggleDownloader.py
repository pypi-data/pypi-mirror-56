# -*- coding: utf-8 -*-
"""Kaggle_dataset_Google_colab

Automatically generated by Colaboratory.

Original file is located at
	https://colab.research.google.com/drive/1APs-Sk2U0TEju6E1_GMip14MR88_BWVz
"""

def get_dataset(kaggle_dataset_api = None):
  """
  download the dataset and unzip the zip files

  Checks: 
  1. upload the kaggle json file obtained from your kaggle account
  2. call the 'get_dataset' function by passing the dataset api as an argument in string format

  """
  if not kaggle_dataset_api:
	kaggle_dataset_api = input('Enter the Kaggle API dataset download link: ')

  !mkdir -p ~/.kaggle
  !cp kaggle.json ~/.kaggle/
  !chmod 600 ~/.kaggle/kaggle.json
  !ls ~/.kaggle

  !ls -l ~/.kaggle
  !cat ~/.kaggle/kaggle.json

  !pip install -q kaggle
  !pip install -q kaggle-cli

  import os
  os.system(kaggle_dataset_api)

  import zipfile
  zipfiles = [file for file in os.listdir() if file.endswith('.zip')]
  for file in zipfiles:
	zipref = zipfile.ZipFile(file)
	zipref.extractall()
	zipref.close()

  print('Zip Files unzipped')
  print('\n', os.listdir())
  res = input('Remove zip files ? (yes/no) :')
  if res == 'yes' or res == 'Y' or res == 'y' or res == 'Yes' or res == 'YES' :
	for file in zipfiles:
	  os.remove(file)
  print('\n', os.listdir())