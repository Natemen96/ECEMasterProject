# %%

model = Sequential()
model.add(LSTM(32, input_shape=(1, 1), return_sequences=True))
model.add(LSTM(16))
model.add(Dropout(0.2))
model.add(Dense(1))
model.add(Activation('linear'))
# model.load_weights('/home/nubonix/PycharmProjects/TimeSeriesPrediction/1611392144.h5')
model.compile(loss='mean_squared_error', optimizer='adagrad')
# %%
model = Sequential()
model.add(LSTM(64, return_sequences = True, input_shape = (10,10)))
model.add(LSTM(48))
model.add(Flatten())
model.add(Dense(32, activation = 'tanh'))
model.add(Dense(5))
# %%
    model = Sequential()
    model.add(Conv2D(kernel_size=(3,3),filters=(12),padding="SAME",input_shape = (inputres,inputres,3), activation = "relu"))#16#12 #Same/Valid
    model.add(Flatten())
    model.add(Dense(outputres*outputres*3, activation = "relu"))#,input_shape = traindatain[1,1:].shape
    opti = optimizers.Adadelta(lr=.1,decay=1e-6)#Changes learning rate.
    model.compile(loss='mean_squared_error', optimizer=opti,metrics=['mae', 'acc'])
    print(model.summary())
# %%
        x = Conv2D(64, (9, 9), activation='relu', padding='same')(input_img)
        x = MaxPooling2D((2, 2), padding='same')(x)
        x = Conv2D(64, (9, 9), activation='relu', padding='same')(x)
        x = MaxPooling2D((2, 2), padding='same')(x)
        x = Flatten()(x)
        encoded = Dense(400,activation = 'relu')(x)
        encoder = Model(input_img, encoded)

        decoder_input= Input((400,))
        decoder = Dense(400, activation = "relu")(decoder_input)
        x = Reshape((1,1,400))(decoder)
        x = UpSampling2D((16, 16))(x)
        x = Conv2D(32, (9, 9), activation='relu', padding='same')(x)
        x = UpSampling2D((4, 4))(x)
        x = Conv2D(32, (9, 9), activation='relu', padding='same')(x)
        x = UpSampling2D((2, 2))(x)
        x = Conv2D(32, (9, 9), activation='relu', padding='same')(x)
        x = UpSampling2D((2, 2))(x)
        decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)
        decoder = Model(decoder_input, decoded)
        
        auto_input = Input(shape=(inputres,inputres,3))
        encoded = encoder(auto_input)
        decoded = decoder(encoded)

        auto_encoder = Model(auto_input, decoded)
        opti = optimizers.adadelta(lr=.07,decay=1e-6)#Changes learning rate.
        auto_encoder.compile(optimizer=opti, loss = 'mean_squared_error',metrics=['mae', 'acc'])
# %%
# %%
# %%
# %%
