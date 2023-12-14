import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
import datetime
import sys
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import yfinance as yf
import Voice_Tools3 as v

def Train_Network():
    # Load and preprocess data
    df = pd.read_csv('mom_data.csv', index_col='Date')
    X = df.drop('target', axis=1).values
    y = df['target'].values
    print(y)

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
    X_train = scaler.transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)

    # Model selection
    best_loss = float('inf')
    for lr in [0.001, 0.01, 0.1]:
        for density in [66, 132, 264]: #32, 64, 128]:
            for batch_size in [16, 32, 64]:
                # model = Sequential()
                # model.add(Dense(density, activation='relu', input_shape=[X_train.shape[1]]))
                # model.add(Dense(1, activation='sigmoid'))
                # model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=lr), metrics=['accuracy'])
                model = Sequential()
                model.add(Dense(density, activation='relu', input_shape=[X_train.shape[1]]))
                model.add(Dense(int(density/2), activation='relu'))
                model.add(Dense(int(density/4), activation='relu'))
                model.add(Dense(1, activation='sigmoid'))
                model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=lr), metrics=['accuracy'])
                model.fit(X_train, y_train,
                          validation_data=(X_val, y_val),
                          epochs=100, batch_size=batch_size, verbose=0)

                val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)

                if val_loss < best_loss:
                    best_loss = val_loss
                    best_lr = lr
                    best_density = density
                    best_batch_size = batch_size

    print('best_loss = ', best_loss)
    model_version = 1
    model_name = f'mom_model_v{model_version}'
    saved_date = datetime.datetime.now().strftime("%Y%m%d")

    artifacts = {
        'model_name': model_name,
        'saved_date': saved_date,
        'model_version': model_version,
        'model': model,
        'scaler': scaler,
        'learning_rate': best_lr
    }

    model_path = 'Z:/StockPrices/models/mom_model_v1.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(artifacts, f)

def Predict_SPY():
    print('Predicting SPY trade')
    # Reload model
    with open(f'models/mom_model_v1.pkl', 'rb') as f:
        artifacts = pickle.load(f)

    best_model = artifacts['model']
    scaler = artifacts['scaler']
    lr = artifacts['learning_rate']

    # New data transforms
    # List of tickers
    tickers = [
        'SPY', 'BIL', 'BWX', 'BWZ', 'CNRG', 'CWB', 'CWI', 'DGT', 'DIA', 'DWX',
        'EBND', 'EDIV', 'EEMX', 'EFAX', 'EMTL', 'EWX', 'FEZ', 'FISR', 'FITE',
        'FLRN', 'GAL', 'GII'
    ]

    # Get most recent Friday
    today = datetime.datetime.today()
    weekday = today.weekday()

    if weekday == 4:
        # If today is Friday, use today's date
        most_recent_friday = today
    else:
        # Calculate the number of days to subtract to get to the most recent Friday
        days_to_subtract = (weekday + 3) % 7
        most_recent_friday = today - datetime.timedelta(days=days_to_subtract)

    # Set start date to 6 weeks ago
    start = most_recent_friday - datetime.timedelta(weeks=6)
    print("start: ", start, "Recent Friday: ", most_recent_friday)

    # Empty dataframe
    momentum = pd.DataFrame()

    # Loop through tickers
    for tick in tickers:
        # Get prices
        prices = yf.Ticker(tick).history(period="6wk", interval="1wk", start=start.strftime('%Y-%m-%d'))
        print(f"Prices for {tick}: {len(prices)} rows")
        prices.index = pd.to_datetime(prices.index)
        prices.index = prices.index.date

        # Save to CSV
        # prices.to_csv(f'{tick}_prices.csv')

        # Check if prices DataFrame is empty or has missing data
        if not prices.empty:
            # Calculate momentum indicators
            mom2 = prices['Close'].diff(periods=2)
            #print(f"Mom2 for {tick}: {len(mom2)} values")
            mom4 = prices['Close'].diff(periods=4)
            #print(f"Mom5 for {tick}: {len(mom5)} values")
            mom6 = prices['Close'].diff(periods=6)
            #print(f"Mom10 for {tick}: {len(mom10)} values")

            #print(tick, 'mom2', mom2, 'mom5', mom5, 'mom10', mom10)

            # Threshold momentum
            mom2_binary = (mom2 >= 0).astype(int)
            mom4_binary = (mom4 >= 0).astype(int)
            mom6_binary = (mom6 >= 0).astype(int)

            #print(tick, 'mom2_binary', mom2_binary, 'mom5_binary', mom5_binary, 'mom10_binary', mom10_binary)

            # Add to dataframe
            momentum[tick + '_mom2'] = mom2_binary
            momentum[tick + '_mom4'] = mom4_binary
            momentum[tick + '_mom6'] = mom6_binary
            #print(f"Momentum before dropping Date: {len(momentum)} rows")

            #print(momentum)

    x_new_data = pd.DataFrame()
    X_new_df = pd.DataFrame(momentum)


    # # # Add date column
    # date_col = 'Date' if 'Date' in momentum.columns else None
    # if date_col == 'Date':
    #     # X_new_data is currently a NumPy array
    #     X_new_data = momentum.drop('Date', axis=1).values
    #     # Convert it to a DataFrame
    #     X_new_df = pd.DataFrame(X_new_data)
    # else:
    #     # Convert it to a DataFrame
    #     X_new_df = pd.DataFrame(momentum)

    # Now you can call to_csv
    X_new_df.to_csv('Z:\StockPrices\Momentum_Data.csv')
    print('saved momentum data')
    # Predictions
    predictions = best_model.predict(X_new_df)  #.reshape(-1)
    print("len of predictions: ", len(predictions))
    prediction_dates = []
    print(predictions)
    for i in range(7, -1, -1):
        date = most_recent_friday - datetime.timedelta(weeks=i)
        prediction_dates.append(date.strftime('%Y-%m-%d'))

    for i in range(0, 8):
        print(str(7 - i) + " weeks ago: " + prediction_dates[i] + ": " + str(int(predictions[i] * 100)) + "%")
    SPYprediction = int(predictions[7] * 100)

    v.Play_Prompt("In 4 weeks there is a " + str(SPYprediction) + " percent chance the SPY index will be up more than 5% from now.", 'spy', 'silent')

    return SPYprediction

#Train_Network()
#Predict_SPY()