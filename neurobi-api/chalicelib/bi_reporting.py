import pandas as pd


# Function to fetch sample business data (e.g., a public dataset)
def fetch_sample_data():
    url = "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"
    df = pd.read_csv(url, encoding='ISO-8859-1')
    return df.head(100)