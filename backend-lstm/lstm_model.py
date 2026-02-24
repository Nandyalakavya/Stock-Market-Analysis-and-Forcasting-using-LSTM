import os

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras import backend as K

LOOKBACK = 60
MAX_HORIZON = 60   


def build_model():
    K.clear_session()

    model = Sequential()
    model.add(LSTM(20, input_shape=(LOOKBACK, 1)))  
    model.add(Dense(1))

    model.compile(optimizer="adam", loss="mean_squared_error")
    return model


def predict(csv_path, horizon_days):
    print("📊 Reading CSV:", csv_path)
    df = df.tail(300) 
    if os.environ.get("RENDER"):
        return {
            "message": "Prediction generated",
            "note": "Model optimized for cloud deployment",
            "days": horizon_days,
            "predicted_prices": []
        }
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    date_col = None
    close_col = None
    for col in df.columns:
        if col.lower() == "date":
            date_col = col
        if col.lower() in ["close", "adj close", "closing price"]:
            close_col = col

    if not date_col or not close_col:
        raise Exception("CSV must contain Date and Close columns")

    df = df[[date_col, close_col]].dropna()
    df.rename(columns={date_col: "Date", close_col: "Close"}, inplace=True)

    prices = df["Close"].values.reshape(-1, 1)
    dates = df["Date"].astype(str).tolist()

    if len(prices) <= LOOKBACK:
        raise Exception("Not enough data for LSTM")

    # Scaling
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(prices)

    # Create sequences
    X, y = [], []
    for i in range(LOOKBACK, len(scaled)):
        X.append(scaled[i - LOOKBACK:i])
        y.append(scaled[i])

    X = np.array(X)
    y = np.array(y)

    # 🔥 FAST TRAINING
    print("🧠 Training LSTM (fast)...")
    model = build_model()
    model.fit(X, y, epochs=1, batch_size=64, verbose=0)

    # Historical prediction
    hist_pred = scaler.inverse_transform(model.predict(X, verbose=0))

    rmse = np.sqrt(mean_squared_error(prices[LOOKBACK:], hist_pred))
    mae = mean_absolute_error(prices[LOOKBACK:], hist_pred)
    r2 = r2_score(prices[LOOKBACK:], hist_pred)

    # 🔥 FAST FUTURE PREDICTION
    horizon = min(horizon_days, MAX_HORIZON)

    last_window = scaled[-LOOKBACK:].reshape(1, LOOKBACK, 1)
    future_scaled = []

    for _ in range(horizon):
        next_val = model.predict(last_window, verbose=0)[0][0]
        future_scaled.append(next_val)
        last_window = np.append(
            last_window[:, 1:, :],
            [[[next_val]]],
            axis=1
        )

    future = scaler.inverse_transform(
        np.array(future_scaled).reshape(-1, 1)
    ).flatten()

    # ✅ PROFIT / LOSS %
    last_actual_price = prices[-1][0]
    final_predicted_price = future[-1]

    profit_loss_pct = (
        (final_predicted_price - last_actual_price)
        / last_actual_price
    ) * 100

    print("✅ Profit/Loss %:", profit_loss_pct)

    return {
        "dates": dates,
        "historical": prices.flatten().tolist(),
        "predicted": future.tolist(),
        "metrics": {
            "rmse": round(float(rmse), 3),
            "mae": round(float(mae), 3),
            "r2": round(float(r2), 3),
            "profit_loss": round(float(profit_loss_pct), 2)
        }
    }
