from tensorflow.keras import backend as K

def evalAccuracy(y_data,y_pred,func):
    acc=K.eval(100*K.sum(func(y_data,y_pred))/len(y_pred))
    print("Your score {}".format(acc))
