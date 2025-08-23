import pandas as pd
import numpy as np
import pymc as pm
import pytensor.tensor as tt
import arviz as az


def run_change_point_model(log_returns, n_change_points=2):
    """Run Bayesian change point model on log returns."""
    n_points = len(log_returns)
    y = log_returns.copy()
    y_mean, y_std = np.mean(y), np.std(y)
    y_stdzd = (y - y_mean) / y_std

    with pm.Model() as model:
        idx = np.arange(n_points)
        alpha = pm.Beta('alpha', alpha=2, beta=2, shape=n_change_points)
        tau = pm.Deterministic('tau', tt.sort(alpha) * n_points)
        seg = tt.sum((idx[:, None] >= tau[None, :]), axis=1)
        mu = pm.Normal('mu', mu=0.0, sigma=0.5, shape=n_change_points + 1)
        sigma = pm.HalfNormal('sigma', sigma=1.0, shape=n_change_points + 1)
        pm.Normal('obs', mu=mu[seg], sigma=sigma[seg], observed=y_stdzd)
        trace = pm.sample(
            draws=1000,
            tune=500,
            chains=4,
            cores=4,
            target_accept=0.95,
            max_treedepth=25,
            init="jitter+adapt_diag",
            return_inferencedata=True
        )
    return trace

def save_results(trace, dates, output_path):
    """Save change point results to CSV."""
    n_points = len(dates)
    tau_samples = trace.posterior['tau'].values
    change_points = np.clip(np.rint(np.mean(tau_samples, axis=(0, 1))).astype(int), 0, n_points - 1)
    change_point_dates = dates[change_points]
    n_bins = min(50, n_points // 10)
    probs = []
    for i in range(len(change_points)):
        hist, bin_edges = np.histogram(tau_samples[:, :, i].flatten(), bins=n_bins, range=(0, n_points), density=True)
        bin_idx = np.digitize(change_points[i], bin_edges) - 1
        bin_idx = np.clip(bin_idx, 0, len(hist) - 1)
        probs.append(hist[bin_idx] * (bin_edges[1] - bin_edges[0]))
    change_point_probs = np.array(probs)

    results = pd.DataFrame({
        'Change_Point_Index': change_points,
        'Change_Point_Date': change_point_dates,
        'Posterior_Probability': change_point_probs
    })
    results.to_csv(output_path, index=False)
    return results

if __name__ == "__main__":
    base_path = '/content/drive/MyDrive/OilShift'
    data_path = f'{base_path}/data/processed/brent_oil_prices_cleaned.csv'
    output_path = f'{base_path}/results/change_point_results.csv'

    df = pd.read_csv(data_path, index_col='Date', parse_dates=True)
    df_semiannual = df.resample('2QE').mean().dropna(subset=['Log_Returns'])
    log_returns = df_semiannual['Log_Returns'].values
    dates = df_semiannual.index

    trace = run_change_point_model(log_returns)
    results = save_results(trace, dates, output_path)
    print("Change Point Results:")
    print(results)
