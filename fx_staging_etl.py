import pandas as pd
import numpy as np

# 1. Generate Raw Cross-Border Transaction Data
np.random.seed(42)
n = 500

df = pd.DataFrame({
    'transaction_id': [f"TXN-{1000+i}" for i in range(n)],
    'transaction_date': pd.date_range(start='2026-01-01', periods=n, freq='h'),
    'foreign_amount': np.random.uniform(100, 5000, n).round(2),
    'currency': np.random.choice(['USD', 'EUR', 'GBP', 'JPY'], size=n, p=[0.4, 0.3, 0.2, 0.1])
})

# 2. Daily FX Rate Lookup Table (Normalized to INR Base)
fx_rates = {
    'USD': 83.50,
    'EUR': 90.20,
    'GBP': 105.80,
    'JPY': 0.55
}

# 3. ETL Staging Engine: Map Rates and Normalize Base Amount
df['fx_rate_to_inr'] = df['currency'].map(fx_rates)
df['base_amount_inr'] = (df['foreign_amount'] * df['fx_rate_to_inr']).round(2)

# 4. Handle Missing/Corrupted Records and Generate Summary Table
df.dropna(inplace=True)

summary_table = df.groupby('currency').agg(
    total_transactions=('transaction_id', 'count'),
    total_foreign_vol=('foreign_amount', 'sum'),
    total_inr_volume=('base_amount_inr', 'sum')
).reset_index()

print("--- FX Staging Data Summary ---")
print(summary_table)
