# forecasting_rfm_images_final_corrected.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# -----------------------------
# Cartella output
# -----------------------------
output_dir = "Metrics"
os.makedirs(output_dir, exist_ok=True)

# -----------------------------
# Caricamento dataset
# -----------------------------
file_path = "Dataset/online_retail_II_cleaned.xlsx"
df = pd.read_excel(file_path, parse_dates=['InvoiceDate'])

# -----------------------------
# Pulizia dati
# -----------------------------
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
df = df.dropna(subset=['InvoiceDate','Quantity','Price','Return'])
df['TotalPrice'] = df['Quantity'] * df['Price']
df['Return'] = df['Return'].str.lower()

# -----------------------------
# Vendite
# -----------------------------
df_sales = df[(df['TotalPrice'] > 0) & (df['Return'] == 'no')]

# -----------------------------
# 1. Forecasting avanzato
# -----------------------------
# Aggregazione giornaliera
df_sales_daily = df_sales.copy()
df_sales_daily['InvoiceDate'] = df_sales_daily['InvoiceDate'].dt.floor('D')  # arrotonda al giorno

# Prophet
sales_ts_prophet = df_sales_daily.groupby('InvoiceDate')['TotalPrice'].sum().reset_index()
sales_ts_prophet.columns = ['ds','y']
prophet_model = Prophet()
prophet_model.fit(sales_ts_prophet)
future = prophet_model.make_future_dataframe(periods=30)
forecast = prophet_model.predict(future)

fig1 = prophet_model.plot(forecast)
plt.title("Forecast Prophet")
fig1.savefig(os.path.join(output_dir,'forecast_prophet.png'))
plt.close()

# ARIMA
sales_ts_arima = df_sales_daily.groupby('InvoiceDate')['TotalPrice'].sum()
sales_ts_arima = sales_ts_arima.asfreq('D', fill_value=0)  # indice continuo
arima_model = ARIMA(sales_ts_arima, order=(5,1,0))
arima_result = arima_model.fit()
arima_forecast = arima_result.forecast(30)

plt.figure(figsize=(10,6))
plt.plot(sales_ts_arima.index, sales_ts_arima.values, label='Vendite Reali')
plt.plot(pd.date_range(start=sales_ts_arima.index.max()+pd.Timedelta(days=1), periods=30),
         arima_forecast, label='Forecast ARIMA', color='red')
plt.xticks(rotation=45)
plt.title("ARIMA Forecast vs Vendite Reali")
plt.xlabel("Data")
plt.ylabel("Vendite Totali")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir,'forecast_arima.png'))
plt.close()

# -----------------------------
# 2. Segmentazione clienti (RFM + KMeans)
# -----------------------------
snapshot_date = df_sales['InvoiceDate'].max() + pd.Timedelta(days=1)
rfm = df_sales.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'Invoice': 'nunique',
    'TotalPrice': 'sum'
}).reset_index()
rfm.columns = ['CustomerID','Recency','Frequency','Monetary']

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['Recency','Frequency','Monetary']])
kmeans = KMeans(n_clusters=4, random_state=42)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

plt.figure(figsize=(8,6))
sns.scatterplot(data=rfm, x='Recency', y='Monetary', hue='Cluster', palette='Set2')
plt.title('RFM Customer Segmentation')
plt.xlabel('Recency')
plt.ylabel('Monetary')
plt.tight_layout()
plt.savefig(os.path.join(output_dir,'rfm_clusters.png'))
plt.close()

# -----------------------------
# 3. Metriche KPI dinamiche
# -----------------------------
df_sales['Month'] = df_sales['InvoiceDate'].dt.to_period('M')
monthly_sales = df_sales.groupby('Month')['TotalPrice'].sum().reset_index()
monthly_sales['YoY_Growth'] = monthly_sales['TotalPrice'].pct_change(12)
monthly_sales['MoM_Growth'] = monthly_sales['TotalPrice'].pct_change(1)
monthly_sales['Rolling_Avg_3'] = monthly_sales['TotalPrice'].rolling(3).mean()

plt.figure(figsize=(10,6))
plt.plot(monthly_sales['Month'].astype(str), monthly_sales['TotalPrice'], label='Vendite Totali')
plt.plot(monthly_sales['Month'].astype(str), monthly_sales['Rolling_Avg_3'], label='Media Mobile 3 mesi')
plt.xticks(rotation=45)
plt.xlabel('Mese')
plt.ylabel('Vendite')
plt.title('Vendite Mensili & Media Mobile')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir,'monthly_sales.png'))
plt.close()

print(f"Analisi completata! Tutti i grafici salvati in '{output_dir}'")
