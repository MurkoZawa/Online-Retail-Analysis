import pandas as pd

# Percorso file di input e output
input_file = "online_retail_II.xlsx"
output_file = "online_retail_II_cleaned.xlsx"

# Carica tutti i fogli del file Excel in un dizionario
sheets = pd.read_excel(input_file, sheet_name=None)

cleaned_sheets = {}

for sheet_name, df in sheets.items():
    # Rimuove duplicati (tutte le colonne uguali)
    df = df.drop_duplicates()

    # Rimuove righe con Quantity nullo o uguale a 0
    df = df.dropna(subset=["Quantity"])
    df = df[df["Quantity"] != 0]

    # Rimuove righe con Price nullo o uguale a 0
    df = df.dropna(subset=["Price"])
    df = df[df["Price"] != 0]

    # Crea la colonna Return
    df["Return"] = df["Quantity"].apply(lambda x: "sì" if x < 0 else "no")

    # Crea la colonna TotalPrice
    df["TotalPrice"] = df["Quantity"] * df["Price"]

    # Assicurati che le colonne chiave siano del tipo corretto
    df["StockCode"] = df["StockCode"].astype(str)
    df["Invoice"] = df["Invoice"].astype(str)
    df["Customer ID"] = df["Customer ID"].astype(str)
    df["Country"] = df["Country"].astype(str)

    # Colonna ProductInTransactions: numero di Invoice per ogni StockCode
    df["ProductInTransactions"] = df.groupby("StockCode")["Invoice"].transform("nunique")

    # Colonna TransactionSize: numero di StockCode per ogni Invoice
    df["TransactionSize"] = df.groupby("Invoice")["StockCode"].transform("nunique")
    
    # CustomerTransactions: numero di Invoice uniche per ogni Customer
    df["CustomerTransactions"]  = df.groupby("Customer ID")["Invoice"].transform("nunique")

    # CountryTransactions: numero di Invoice uniche per ogni Country
    df["CountryTransactions"] = df.groupby("Country")["Invoice"].transform("nunique")
    
    # CountrySales: somma TotalPrice per Country
    df["CountrySales"] = df.groupby("Country")["TotalPrice"].transform("sum")

    # Salva il foglio pulito
    cleaned_sheets[sheet_name] = df

# Scrive il nuovo file Excel con entrambi i fogli
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for sheet_name, df in cleaned_sheets.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print("File pulito creato con successo:", output_file)
