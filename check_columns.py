
import pandas as pd
import os

folder = "data"

for file in os.listdir(folder):
    if file.endswith(".csv"):
        path = os.path.join(folder, file)

        df = pd.read_csv(path)

        print("\n" + "=" * 40)
        print("FILE:", file)
        print("Columns:", list(df.columns))
        print("=" * 40)
