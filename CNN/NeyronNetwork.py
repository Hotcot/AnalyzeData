from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, MaxPooling1D, Conv1D, GlobalMaxPooling1D, Dropout
from tensorflow.keras import utils
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import utils
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class NeyronNetwork:
    
    __num_words = 10000
    __max_news_len = 100
    __nb_classes = 4
    
    #data for training neyron network
    __train = pd.read_csv('train.csv',
                          header = None,
                          names = ['class', 'title', 'text'])
    
    def __init__(self):     
        tokenizer, model_cnn = self.__train_and_test_cnn()
        self.__classification_data(tokenizer, model_cnn)
    
    
    def __train_and_test_cnn(self):
        news = self.__select_data_for_training()
        
        y_train = self.__select_true_answer()
        
        # #create tokenizer Keras
        tokenizer = Tokenizer(num_words = self.__num_words)
        
        # train the tokenizer on the news
        tokenizer.fit_on_texts(news)
        
        # Converting news to a numeric representation
        sequences = self.__convert_news_to_numeric(tokenizer, news)
        print(sequences)
        
        # Limiting the length of reviews
        x_train = self.__limitted_length_news(sequences)
        print(x_train[:5])
        
        model_cnn = self.__create_cnn()
        
        model_cnn_save_path = self.__create_callback_save_nn(x_train, y_train, model_cnn)
        print(model_cnn_save_path)
        
        test = self.__select_data_for_test()
        test_sequences = tokenizer.texts_to_sequences(test['text'])
        
        test_sequences = self.__convert_news_to_numeric(tokenizer, test['text'])
        x_test = pad_sequences(test_sequences, maxlen = self.__max_news_len)
        y_test = utils.to_categorical(test['class']-1, self.__nb_classes)
        print(y_test)
        model_cnn.load_weights(model_cnn_save_path)
        model_cnn.evaluate(x_test, y_test, verbose=1)
        
        return tokenizer, model_cnn
        
    
    def __select_data_for_training(self):
        news = self.__train['text']
        return news
    
    def __select_true_answer(self):
        y_train = utils.to_categorical(self.__train['class']-1, self.__nb_classes)
        return y_train
    
    def __convert_news_to_numeric(self, tokenizer, news):
        return tokenizer.texts_to_sequences(news)
    
    def __limitted_length_news(self, sequences):
        return pad_sequences(sequences, maxlen = self.__max_news_len)
    
    def __create_cnn(self):
        model_cnn = Sequential()
        model_cnn.add(Embedding(self.__num_words, 32, input_length = self.__max_news_len))
        model_cnn.add(Conv1D(250, 5, padding='valid', activation='relu'))
        model_cnn.add(GlobalMaxPooling1D())
        model_cnn.add(Dense(128, activation='relu'))
        model_cnn.add(Dense(4, activation='softmax'))
        
        model_cnn.compile(optimizer='adam', 
                        loss='categorical_crossentropy', 
                        metrics=['accuracy'])
        
        model_cnn.summary()
        
        return model_cnn
    
    def __create_callback_save_nn(self, x_train, y_train, model_cnn):
        model_cnn_save_path = 'best_model_cnn.h5'
        # checkpoint_callback_cnn = ModelCheckpoint(model_cnn_save_path, 
        #                                     monitor='val_accuracy',
        #                                     save_best_only=True,
        #                                     verbose=1)
        
        # history_cnn = model_cnn.fit(x_train, 
        #                             y_train, 
        #                             epochs=5,
        #                             batch_size=128,
        #                             validation_split=0.1,
        #                             callbacks=[checkpoint_callback_cnn])
        
        # self.__show_graphics_train(history_cnn)
        
        return model_cnn_save_path
      
        
    def __show_graphics_train(self, history_cnn):
        plt.plot(history_cnn.history['accuracy'], 
                label='Частка вірних відповідей на навчальному наборі')
        plt.plot(history_cnn.history['val_accuracy'], 
                label='Частка вірних відповідей на перевірочному наборі')
        plt.xlabel('Епоха навчання')
        plt.ylabel('Частка вірних відповідей')
        plt.legend()
        plt.show()
        
    def __select_data_for_test(self):
        test = pd.read_csv('test.csv', 
                    header=None,
                    names=['class', 'title', 'text'])
        return test
    
    def __classification_data(self, tokenizer, model_cnn):
        current_data = self.__select_data_for_classification()
        
        current_sequences = tokenizer.texts_to_sequences(current_data['text'])
        data = pad_sequences(current_sequences, maxlen=self.__max_news_len)
        result = model_cnn.predict(data)
        print(result)

        print("max \n")

        for item in range(len(result)):
            # print(item)
            res = np.amax(result[item])
            print(f"{res}")
        
    
    def __select_data_for_classification(self):
        current_data = pd.read_csv('current.csv', 
                        header=None,
                        names=['class', 'title', 'text'])
        return current_data    