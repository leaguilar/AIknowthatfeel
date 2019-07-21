from keras.models import load_model
import tensorflow as tf
import numpy as np
import pickle
import os

class WojakEntity:
    def __init__(self):
    
        self.graph = tf.get_default_graph()
        self.model=load_model("models/model.h5")
    
        
        #FROM Ugly Example preprocessing
        self.pad_char=0
        self.start_char=1
        self.oov_char=2
        self.index_from=3
        max_conv_length=50
        self.encoded=np.full((max_conv_length,1), self.pad_char)

        with open('models/wordDictionary.pkl', 'rb') as handle:
            self.wordDict = pickle.load(handle)    
    def perceive(self,text1,text2,text3):
        print("PERCEIVE")
        self.encoded=self.encodeData(text1,text2,text3)       
    def act(self):
        #global graph
        with self.graph.as_default():
            print("ACT")
            print(self.encoded)
            result=self.model.predict(self.encoded)
            mood=np.argmax(result)
            print("MOOD ",mood)
            if mood == 0:
                return 'others'
            elif mood == 1:
                return 'happy'
            elif mood == 2:
                return 'angry'
            elif mood == 3:
                return 'sad'
            else:
                raise Exception()    
    ################
    
    #Ugly Example preprocessing
    def encodeList(self,text_list,vocab_size,max_conv_length):
        encoded=np.full((max_conv_length,1), self.pad_char)
        if len(text_list)>max_conv_length:
            start_pos=0
        else:
            start_pos=max_conv_length-len(text_list)
        encoded[start_pos]=self.start_char
        for i,w in enumerate(text_list):
            val=self.wordDict.get(w,self.oov_char-self.index_from)+self.index_from
            if val>=vocab_size:
                val=vocab_size-1
            if start_pos+i+1 == max_conv_length:
                break
            encoded[start_pos+i+1]=val

        return encoded.transpose()
           
    def encodeData(self,text1,text2,text3,vocab_size = 5000, max_conv_length=50):
        text=text1+' ### '+text2+' ### '+text3
        text_list=text.split()
        encoded=self.encodeList(text_list,vocab_size,max_conv_length)
        return encoded   
