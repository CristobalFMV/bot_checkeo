from sklearn.datasets import load_diabetes
import pandas as pd

# Cargar dataset
diabetes = load_diabetes()

# Convertir a DataFrame
df = pd.DataFrame(data=diabetes.data, columns=diabetes.feature_names)
df["target"] = diabetes.target

# Mostrar primeras filas
print(df.head())
print(df.describe())
