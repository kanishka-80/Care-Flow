import pandas as pd

def load_data(file_path):
    """Load hospital patient event data."""
    df = pd.read_csv(file_path)
    return df

def inspect_data(df):
    """Display basic information about the dataset."""
    print("Dataset shape:", df.shape)
    print("\nColumn names:")
    print(df.columns.tolist())
    print("\nMissing values:")
    print(df.isnull().sum())

if __name__ == "__main__":
    print("CareFlow data cleaning module is ready.")