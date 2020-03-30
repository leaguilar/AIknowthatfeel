import tensorflow.keras.backend as K

class EvaluateModel:
    def evalAccuracy(self,y_data,y_pred,func):
        acc=K.eval(100*K.sum(func(y_data,y_pred))/len(y_pred))
        print(acc)
