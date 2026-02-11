import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# --- OPZIONI DISPONIBILI ---
options = [
    "Tutti i grafici",
    "Grafici temporali",
    "Grafici di entità"
]

print("Seleziona il tipo di grafici da generare:")
for i, opt in enumerate(options):
    print(f"{i} - {opt}")

try:
    choice = int(input("Inserisci il numero: "))
    if choice < 0 or choice >= len(options):
        raise ValueError
except ValueError:
    print("Errore: scelta non valida.")
    sys.exit()

print(f"Hai scelto: {options[choice]}")

# --- FILE IN INPUT ---
input_file = "Dataset/online_retail_II_cleaned.xlsx"

# --- LETTURA DATI ---
sheets = pd.read_excel(input_file, sheet_name=None)
df = pd.concat(sheets.values(), ignore_index=True)

# --- PREPROCESSING DELLE DATE ---
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)
df["Month"] = df["InvoiceDate"].dt.month
df["Year"] = df["InvoiceDate"].dt.year

# --- SOLO VENDITE ---
sales_df = df[df["Return"] == "no"]

# -------------------------------------------------------
# --- FUNZIONE GRAFICI TEMPORALI ---
# ------------------------------------------------------- 
def generate_temporal_charts(df, sales_df): 
    temporal_dir = "Charts/Temporal Analysis" 
    os.makedirs(temporal_dir, exist_ok=True) 
    all_yearmonths = sorted(df["YearMonth"].unique()) 
    tick_indices = list(range(0, len(all_yearmonths), 2)) 
    tick_labels = [all_yearmonths[i] for i in tick_indices] 
    
    # 1. Fatturato mensile 
    monthly_revenue = sales_df.groupby("YearMonth")["TotalPrice"].sum().sort_index() 
    plt.figure() 
    monthly_revenue.plot() 
    plt.xlabel("Year-Month") 
    plt.ylabel("Total Revenue") 
    plt.title("Monthly Revenue") 
    plt.xticks(ticks=tick_indices, labels=tick_labels, rotation=45, fontsize=8) 
    plt.tight_layout() 
    plt.savefig(f"{temporal_dir}/monthly_revenue.jpg", dpi=300) 
    plt.close() 
    
    # 2. Stagionalità 
    monthly_year_revenue = sales_df.groupby(["Year", "Month"])["TotalPrice"].sum().reset_index() 
    seasonality = monthly_year_revenue.groupby("Month")["TotalPrice"].mean() 
    plt.figure() 
    seasonality.plot(kind="bar") 
    plt.xlabel("Month (1-12)") 
    plt.ylabel("Average Monthly Revenue") 
    plt.title("Average Revenue per Month (Seasonality)") 
    plt.tight_layout() 
    plt.savefig(f"{temporal_dir}/average_monthly_revenue_seasonality.jpg", dpi=300) 
    plt.close() 
    
    # 3. Numero di transazioni per anno-mese 
    monthly_transactions = df.groupby("YearMonth")["Invoice"].nunique().sort_index() 
    plt.figure() 
    monthly_transactions.plot() 
    plt.xlabel("Year-Month") 
    plt.ylabel("Number of Transactions") 
    plt.title("Number of Transactions Over Time") 
    plt.xticks(ticks=tick_indices, labels=tick_labels, rotation=45, fontsize=8) 
    plt.tight_layout() 
    plt.savefig(f"{temporal_dir}/monthly_transactions.jpg", dpi=300) 
    plt.close()
    
    # 4. Valore medio transazione per anno-mese
    avg_transaction_value = df.groupby('YearMonth').apply(
        lambda x: x['TotalPrice'].sum() / x['Invoice'].nunique()
        ).reset_index(name='Fatturato_Medio_per_Transazione')
    avg_transaction_value.plot() 
    plt.xlabel("Year-Month") 
    plt.ylabel("Average Transaction Value") 
    plt.title("Average Transaction Value Over Time") 
    plt.xticks(ticks=tick_indices, labels=tick_labels, rotation=45, fontsize=8) 
    plt.tight_layout() 
    plt.savefig(f"{temporal_dir}/average_transaction_value.jpg", dpi=300) 
    plt.close() 
    
    # 5. Percentuale resi per anno-mese
    monthly_returns = df[df["Return"] == "sì"].groupby("YearMonth")["Invoice"].count() 
    monthly_total_transactions = df.groupby("YearMonth")["Invoice"].count() 
    return_percentage = ((monthly_returns / monthly_total_transactions) * 100).fillna(0).sort_index() 
    plt.figure() 
    return_percentage.plot() 
    plt.xlabel("Year-Month") 
    plt.ylabel("Return Percentage (%)") 
    plt.title("Return Percentage Over Time") 
    plt.xticks(ticks=tick_indices, labels=tick_labels, rotation=45, fontsize=8) 
    plt.tight_layout() 
    plt.savefig(f"{temporal_dir}/return_percentage.jpg", dpi=300) 
    plt.close() 
    print("Grafici temporali salvati nella cartella:", temporal_dir)

# -------------------------------------------------------
# --- FUNZIONE GRAFICI DI ENTITA' ---
# -------------------------------------------------------
def generate_entity_charts(df):
    base_dir = "Charts/Entity Analysis"
    os.makedirs(base_dir, exist_ok=True)

    sales_df = df[df["Return"] == "no"]

    # =========================
    # --- ANALISI DEL PRODOTTO ---
    # =========================
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Fatturato totale per prodotto
    sales_df.groupby("StockCode")["TotalPrice"].sum() \
        .sort_values(ascending=False).head(10).plot(
            kind="bar", ax=axes[0], title="Top Products by Revenue"
        )

    # 2. Transazioni per prodotto
    sales_df.groupby("StockCode")["Invoice"].nunique() \
        .sort_values(ascending=False).head(10).plot(
            kind="bar", ax=axes[1], title="Top Products by Transactions"
        )

    # 3. Percentuale resi per prodotto
    total_product_rows = df.groupby("StockCode").size()
    returned_product_rows = df[df["Return"] == "sì"].groupby("StockCode").size()
    prod_return_percent = (returned_product_rows / total_product_rows * 100).fillna(0)
    prod_return_percent.sort_values(ascending=False).head(20).plot(
        kind="bar", ax=axes[2], title="Top Products by Return %"
    )


    fig.suptitle("Product Analysis", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(f"{base_dir}/product_analysis.jpg", dpi=300)
    plt.close()

    # =========================
    # --- ANALISI DEL CLIENTE ---
    # =========================
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Filtra i clienti validi (Customer ID diverso da "non indicato")
    valid_customers_df = sales_df[sales_df["Customer ID"] != "non indicato"]

    # 1. Fatturato totale per cliente
    valid_customers_df.groupby("Customer ID")["TotalPrice"].sum() \
        .sort_values(ascending=False).head(10).plot(
            kind="bar", ax=axes[0], title="Top Customers by Revenue"
        )

    # 2. Transazioni per cliente
    df[df["Customer ID"] != "non indicato"].groupby("Customer ID")["Invoice"].nunique() \
        .sort_values(ascending=False).head(10).plot(
            kind="bar", ax=axes[1], title="Top Customers by Transactions"
        )

    # 3. Clienti che in media spendono di più per transazione 
    top_customers = (
        df.groupby("Customer ID")
          .apply(lambda x: x["TotalPrice"].sum() / x["Invoice"].nunique())
          .reset_index(name="Avg Client Transaction Value")
          .sort_values("Avg Client Transaction Value", ascending=False)
          .head(10)
    )
    top_customers.plot(kind="bar", ax=axes[2], title="Top Customers by Avg Transaction Value")

    fig.suptitle("Customer Analysis", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(f"{base_dir}/customer_analysis.jpg", dpi=300)
    plt.close()

    # =========================
    # --- ANALISI DEL PAESE ---
    # =========================
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Fatturato totale per paese
    sales_df.groupby("Country")["TotalPrice"].sum() \
        .sort_values(ascending=False).head(10).plot(
            kind="bar", ax=axes[0], title="Top Countries by Revenue"
        )

    # 2. Numero di transazioni per paese
    df.groupby("Country")["Invoice"].nunique() \
        .sort_values(ascending=False).head(10).plot(
            kind="bar", ax=axes[1], title="Top Countries by Transactions"
        )

    # 3. Percentuale resi per paese
    total_country_rows = df.groupby("Country").size()
    returned_country_rows = df[df["Return"] == "sì"].groupby("Country").size()
    country_return = (returned_country_rows / total_country_rows * 100).fillna(0)
    country_return.sort_values(ascending=False).head(10).plot(
        kind="bar", ax=axes[2], title="Top Countries by Return %"
    )

    fig.suptitle("Country Analysis", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(f"{base_dir}/country_analysis.jpg", dpi=300)
    plt.close()

    print("Grafici di entità salvati in:", base_dir)



# -------------------------------------------------------
# --- ESECUZIONE ---
# -------------------------------------------------------
if choice == 0:
    generate_temporal_charts(df, sales_df)
    generate_entity_charts(df)
elif choice == 1:
    generate_temporal_charts(df, sales_df)
elif choice == 2:
    generate_entity_charts(df)
    

