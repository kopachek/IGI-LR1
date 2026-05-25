import pandas as pd

def categorize():
    df = pd.read_csv('T6\\SuperMarketAnalysis.csv')

    unique_products = df['Product line'].unique()
    cat_type = pd.api.types.CategoricalDtype(categories=sorted(unique_products), ordered=True)

    product_series = df['Product line'].astype(cat_type)
    product_codes = product_series.cat.codes

    result_df = pd.DataFrame({
        'Code': product_codes,
        'Product Name': product_series
    })

    result_df.to_csv('T6\\ResCategorize.csv', index=False, encoding='utf-8-sig')

def analyze_coeff():
    df = pd.read_csv('T6\\SuperMarketAnalysis.csv')

    df['Hour'] = pd.to_datetime(df['Time'], format='%I:%M:%S %p').dt.hour

    hourly_avg = df.groupby('Hour')['Sales'].mean()

    max_avg = hourly_avg.max()
    min_avg = hourly_avg.min()

    ratio = max_avg / min_avg

    print(f"Avg sales in the most profitable hour: {max_avg:.2f}")
    print(f"Avg sales at the least profitable hour: {min_avg:.2f}")
    print(f"Ratio: {round(ratio, 2)}")

def task_6():
    categorize()
    analyze_coeff()

if __name__ == "__main__":
    task_6()