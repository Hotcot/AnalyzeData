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
    __max_news_len = 500
    __nb_classes = 4
    
    #data for training neyron network
    __train = pd.read_csv('train.csv',
                          header = None,
                          names = ['class', 'title', 'text'])
    
    def __init__(self):    
         
        tokenizer, model_cnn, model_cnn_save_path = self.__train_and_test_cnn()
        
        self.__classification_data(tokenizer, model_cnn, model_cnn_save_path)
    
    
    def __train_and_test_cnn(self):
        #emit data for training
        news = self.__select_data_for_training()
        #Emit true answer
        y_train = self.__select_true_answer()
        
        #create tokenizer Keras
        tokenizer = self.__create_tokenizer(news)
        
        # Converting news to a numeric representation
        sequences = self.__convert_news_to_numeric(tokenizer, news)
        
        # Limiting the length of reviews
        x_train = self.__limitted_length_news(sequences)
        
        # create cnn
        model_cnn = self.__create_cnn()        
        model_cnn_save_path = self.__create_callback_save_nn(x_train, y_train, model_cnn)
               
        self.__testing_cnn(tokenizer, model_cnn, model_cnn_save_path)
        
        return tokenizer, model_cnn, model_cnn_save_path
        
    
    def __select_data_for_training(self):
        news = self.__train['text']
        return news
    
    def __select_true_answer(self):
        return utils.to_categorical(self.__train['class']-1, self.__nb_classes)
    
    def __create_tokenizer(self, news):
        tokenizer = Tokenizer(num_words = self.__num_words)
        tokenizer.fit_on_texts(news)
        return tokenizer
        
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
        #                             epochs=3,
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
    
    def __testing_cnn(self, tokenizer, model_cnn, model_cnn_save_path):
        test = self.__select_data_for_test()
        test_sequences = tokenizer.texts_to_sequences(test['text'])
        
        test_sequences = self.__convert_news_to_numeric(tokenizer, test['text'])
        
        x_test = pad_sequences(test_sequences, maxlen = self.__max_news_len)
        y_test = utils.to_categorical(test['class']-1, self.__nb_classes)
        
        model_cnn.load_weights(model_cnn_save_path)
        model_cnn.evaluate(x_test, y_test, verbose=1)   
             
    
    def __classification_data(self, tokenizer, model_cnn, model_cnn_save_path):
        current_data = self.__select_data_for_classification()
        
        model_cnn.load_weights(model_cnn_save_path)
        
        current_sequences = tokenizer.texts_to_sequences(current_data['text'])
        data = pad_sequences(current_sequences, maxlen=self.__max_news_len)
        result = model_cnn.predict(data)
        print(result)

        print("max \n")
        self.__check_true_answer_classification(result)

    def __select_data_for_classification(self):
        current_data = pd.read_csv('current.csv', 
                        header=None,
                        names=['class', 'title', 'id_article', 'link', 'text'])
        return current_data   
    
    def __check_true_answer_classification(self, result):
        for item in range(len(result)):
            
            res = np.amax(result[item])
            
            for col in range(len(result[item])): 
                               
                if(result[item][col] == res):
                    print(f"{col+1}\n{res}")