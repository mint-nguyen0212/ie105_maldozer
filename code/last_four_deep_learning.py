

import numpy as np
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.utils import np_utils
from tensorflow.keras.optimizers import RMSprop
import matplotlib.pyplot as plt

from set_constant import sentences_append
from set_constant import train_path,test_path
from set_constant import save_model_path,L,K
from set_constant import filter_count, kernel_size_,first_neuron_count,dropout,epochs_,batch_size_,validation_split_

# x_train, x_test are (2D) numpy matrices of shape train_apk_count*(L*K)
# Note: each L*K matrix should be flattened into a (L*K) vector
# y_train, y_test are (1D) numpy matrices of shape test_apk_count*1
def get_onetype(path,model,type=0):
    sentences=[]
    names=sentences_append(sentences,path)
    y_=[type]*len(names)
    x_=[]
    for i in sentences:
        x=[]
        for j in i:
            x.extend(model[j])
        x_.extend(x)
    return x_,y_,len(names)

# Get the feature matrices of all APKs under the given path, along with their classifications
def get_apks_and_types (path,TYPE,TYPE_line,type_map,model):
    apk_count=0
    X=[]
    Y=[]
    # Read all training set matrices into this 2D tensor
    for i in range(0,TYPE):
        x,y,z=get_onetype(path+'/'+TYPE_line[i],model,type_map[TYPE_line[i]])
        x=np.array(x)
        X.extend(x)
        Y.extend(y)
        apk_count+=z
    X=np.array(X)
    X= X.reshape((apk_count, L , K, 1))
    print('X shape:', X.shape)
    #X= X.reshape(X.shape[0],L,K,1)
    Y=np.array(Y)
    Y= Y.reshape((apk_count, 1))
    print('X shape:', X.shape)
    
   
   
   
    Y = np_utils.to_categorical(Y, TYPE)
    #Y= Y.reshape((apk_count, 2,1))
    return X,Y,apk_count

def deep_learning(TYPE,TYPE_line,type_map,word2vec_model):
	
	# Training set, test set
	# Not sure about the difference between (a,b,c) and (a,b,c,1) tensors; reshaping input to match the neural network's expected shape to be safe
	x_train,y_train,train_apk_count = get_apks_and_types(train_path,TYPE,TYPE_line,type_map,word2vec_model)
	x_test,y_test,test_apk_count = get_apks_and_types(test_path,TYPE,TYPE_line,type_map,word2vec_model)
	x_train = x_train.astype('float32')
	x_test = x_test.astype('float32')
	x_train /= 255
	x_test /= 255
	#print('x_train shape:', x_train.shape)
	#print('x_test shape:', x_test.shape)

	# Neural network
	model = Sequential()
	# Convolution
	model.add(layers.Conv2D(filters=filter_count, kernel_size=kernel_size_, activation='relu', input_shape=(L , K, 1)))
	model.summary()
	# Pooling
	model.add(layers.MaxPooling2D())
	model.summary()
	# First fully connected layer
	model.add(layers.Dense(units=first_neuron_count, activation='relu'))
	model.summary()
	# Regularization (Dropout)
	model.add(layers.Dropout(dropout))
	model.add(layers.Flatten())
	# Second fully connected layer
	model.add(layers.Dense(units=TYPE, activation='softmax'))
	model.summary()

	model.compile(optimizer=RMSprop(lr=1e-4),
			loss='binary_crossentropy',
				  metrics=['acc'])

	history = model.fit(x_train, y_train,
						epochs=epochs_,
						batch_size=batch_size_,
						validation_split=validation_split_)

	model.save(save_model_path)

	# Plot results
	acc = history.history['acc']
	val_acc = history.history['val_acc']
	loss = history.history['loss']
	val_loss = history.history['val_loss']

	epochs = range(len(acc))

	plt.plot(epochs, acc, 'bo', label='Training acc')
	plt.plot(epochs, val_acc, 'b', label='Validation acc')
	plt.title('Training and validation accuracy')
	plt.legend()

	plt.figure()

	plt.plot(epochs, loss, 'bo', label='Training loss')
	plt.plot(epochs, val_loss, 'b', label='Validation loss')
	plt.title('Training and validation loss')
	plt.legend()
	
	# Test set evaluation
	test_loss, test_acc = model.evaluate(x_test, y_test)
	print('Testing and accuracy:', test_acc)
	
	plt.show()

	
	
	print("Having finished fourth stop:deep learning!")

if __name__ == "__main__":

	from gensim.models import Word2Vec
	from set_constant import TYPE,TYPE_list,type_map
	from set_constant import word2vec_model_path


	word2vec_model = Word2Vec.load(word2vec_model_path)
	deep_learning(TYPE,TYPE_list,type_map,word2vec_model)
