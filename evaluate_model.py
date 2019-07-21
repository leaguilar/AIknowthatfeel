#!/usr/bin/env python

from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.metrics import categorical_accuracy
import pickle
from libs.easeml import evalAccuracy
import argparse

#Ugly Example preprocessing
pad_char=0
start_char=1
oov_char=2
index_from=3

with open('models/wordDictionary.pkl', 'rb') as handle:
    wordDict = pickle.load(handle)

def encodeList(text_list,vocab_size):
    encoded=[start_char]
    for w in text_list:
        val=wordDict.get(w,oov_char-index_from)+index_from
        if val>=vocab_size:
            val=vocab_size-1
        encoded.append(val)
    return encoded
       
def encodeData(data,vocab_size = 5000):
    data_out=[]
    for index, row in data.iterrows():
        text=(row.iloc[0]+' ### '+row.iloc[1]+' ### '+row.iloc[2])
        text_list=text.split()
        encoded=encodeList(text_list,vocab_size)
        data_out.append(encoded)
    return np.array(data_out)
def encodedLabels(data):
    data_out=[]
    for index, row in data.iterrows():
        if row.iloc[0] == 'others':
            data_out.append([1,0,0,0])
        elif row.iloc[0] == 'happy':
            data_out.append([0,1,0,0])
        elif row.iloc[0] == 'angry':
            data_out.append([0,0,1,0])
        elif row.iloc[0] == 'sad':
            data_out.append([0,0,0,1])
        else:
            raise Exception()
    return np.array(data_out).astype(int)
def prepare_data(x_data,max_conv_length):
    x_data = sequence.pad_sequences(x_data, maxlen=max_conv_length)
    return x_data
def loadAndPrepareData(fname,vocab_size=5000,max_conv_length=50):
    data = pd.read_csv(fname,sep='	',header=None)
    x_data_raw=data.filter([1,2,3], axis=1).copy(deep=True)
    y_data_raw=data.filter([4], axis=1).copy(deep=True)  
    x_data = encodeData(x_data_raw,vocab_size)
    y_data = encodedLabels(y_data_raw)
    x_data = prepare_data(x_data,max_conv_length)                       
    return x_data,y_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate Model')
    parser.add_argument('datasetName')
    parser.add_argument('inputPath')
    datasetName=parser.parse_args().datasetName
    inputPath=parser.parse_args().inputPath
    
    fname=inputPath+datasetName
    x_data,y_data=loadAndPrepareData(fname)

    outpath='models/'
    model=load_model(outpath+"model.h5")

    y_pred=model.predict(x_data)
    
    #Pass predicted values to the evaluator
    evalAccuracy(y_data,y_pred,categorical_accuracy)
