import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import axios from 'axios';
import moment from 'moment';
import './App.css';

const App = () => {
  const [prices, setPrices] = useState({ dates: [], prices: [], log_returns: [], volatility: [] });
  const [events, setEvents] = useState([]);
  const [changePoints, setChangePoints] = useState([]);
  const [indicators, setIndicators] = useState([]);
  const [startDate, setStartDate] = useState('1987-01-01');
  const [endDate, setEndDate] = useState('2022-12-31');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, [startDate, endDate]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    const baseUrl = 'http://127.0.0.1:5000/api';
    try {
      const pricesRes = await axios.get(`${baseUrl}/prices`, {
        params: { start: startDate, end: endDate },
      });
      setPrices(pricesRes.data);
      const eventsRes = await axios.get(`${baseUrl}/events`);
      setEvents(eventsRes.data);
      const changePointsRes = await axios.get(`${baseUrl}/change_points`);
      setChangePoints(changePointsRes.data);
      const indicatorsRes = await axios.get(`${baseUrl}/key_indicators`);
      setIndicators(indicatorsRes.data);
    } catch (err) {
      setError('Failed to fetch data. Please check if the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const chartData = prices.dates.map((date, index) => ({
    date,
    price: prices.prices[index],
    log_return: prices.log_returns[index],
    volatility: prices.volatility[index],
  }));

  return (
    <div className="app-container">
      <header className="header">
        <h1>OilShift: Brent Oil Price Dashboard</h1>
        <p>Explore price trends, volatility, and key events (1987–2022)</p>
      </header>
      <div className="filters">
        <div className="filter-group">
          <label>Start Date:</label>
          <input
            type="date"
      value={startDate}
      onChange={(e) => setStartDate(e.target.value)}
      min="1987-01-01"
      max="2022-12-31"
    />
  </div>
  <div className="filter-group">
    <label>End Date:</label>
    <input
      type="date"
      value={endDate}
      onChange={(e) => setEndDate(e.target.value)}
      min="1987-01-01"
      max="2022-12-31"
    />
  </div>
  <button
    className="reset-button"
    onClick={() => {
      setStartDate('1987-01-01');
      setEndDate('2022-12-31');
    }}
  >
    Reset Filters
  </button>
</div>
      {loading && <p className="loading">Loading data...</p>}
      {error && <p className="error">{error}</p>}
      {!loading && !error && (
        <>
          <section className="chart-section">
            <h2>Price and Volatility Trends</h2>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                <XAxis dataKey="date" stroke="#333" />
                <YAxis stroke="#333" />
                <Tooltip
                  formatter={(value, name) => [
                    name === 'price' ? `$${value.toFixed(2)}` : value.toFixed(4),
                    name === 'price' ? 'Price' : 'Volatility',
                  ]}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="price"
                  stroke="#4a90e2"
                  name="Price ($)"
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="volatility"
                  stroke="#28a745"
                  name="Volatility"
                  dot={false}
                />
                {events.map((event, index) => (
                  <ReferenceLine
                    key={`event-${index}`}
                    x={moment(event.Date).format('YYYY-MM-DD')}
                    stroke="#007bff"
                    strokeDasharray="3 3"
                    label={{
                      value: event.Event,
                      position: 'top',
                      fill: '#007bff',
                      fontSize: 12,
                    }}
                  />
                ))}
                {changePoints.map((cp, index) => (
                  <ReferenceLine
                    key={`cp-${index}`}
                    x={moment(cp.Change_Point_Date).format('YYYY-MM-DD')}
                    stroke="#dc3545"
                    strokeDasharray="5 5"
                    label={{
                      value: `Change Point ${index + 1}`,
                      position: 'top',
                      fill: '#dc3545',
                      fontSize: 12,
                    }}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </section>
          <section className="indicators-section">
            <h2>Key Indicators Around Events</h2>
            <table>
              <thead>
                <tr>
                  <th>Event</th>
                  <th>Date</th>
                  <th>Avg Price Change</th>
                  <th>Volatility</th>
                </tr>
              </thead>
              <tbody>
                {indicators.map((ind, index) => (
                  <tr key={index}>
                    <td>{ind.event}</td>
                    <td>{ind.date}</td>
                    <td>{ind.avg_price_change.toFixed(4)}</td>
                    <td>{ind.volatility.toFixed(4)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        </>
      )}
    </div>
  );
};

export default App;
