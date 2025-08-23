from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load data (adjust paths)
base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(base_path, 'data/processed/brent_oil_prices_cleaned.csv')
events_path = os.path.join(base_path, 'data/raw/key_events.csv')
change_point_path = os.path.join(base_path, 'results/change_point_results.csv')

df = pd.read_csv(data_path, index_col='Date', parse_dates=True)
events = pd.read_csv(events_path, parse_dates=['Date'])
change_points = pd.read_csv(change_point_path, parse_dates=['Change_Point_Date'])

# Compute Log_Returns if not present
if 'Log_Returns' not in df.columns:
    df['Log_Returns'] = np.log(df['Price'] / df['Price'].shift(1))
df['Volatility'] = df['Log_Returns'].rolling(window=30).std()
df = df.dropna()

@app.route('/api/prices', methods=['GET'])
def get_prices():
    start = request.args.get('start')
    end = request.args.get('end')
    filtered_df = df
    if start:
        filtered_df = filtered_df[filtered_df.index >= datetime.fromisoformat(start)]
    if end:
        filtered_df = filtered_df[filtered_df.index <= datetime.fromisoformat(end)]
    return jsonify({
        'dates': filtered_df.index.strftime('%Y-%m-%d').tolist(),
        'prices': filtered_df['Price'].tolist(),
        'log_returns': filtered_df['Log_Returns'].tolist(),
        'volatility': filtered_df['Volatility'].tolist()
    })

@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(events.to_dict('records'))

@app.route('/api/change_points', methods=['GET'])
def get_get_change_points():
    return jsonify(change_points.to_dict('records'))

@app.route('/api/key_indicators', methods=['GET'])
def get_key_indicators():
    event_dates = events['Date'].tolist()
    indicators = []
    for event_date in event_dates:
        window = df[(df.index >= event_date - pd.Timedelta(days=30)) & (df.index <= event_date + pd.Timedelta(days=30))]
        if not window.empty:
            indicators.append({
                'event': events[events['Date'] == event_date]['Event'].values[0],
                'date': event_date.strftime('%Y-%m-%d'),
                'avg_price_change': window['Log_Returns'].mean(),
                'volatility': window['Volatility'].mean()
            })
    return jsonify(indicators)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
