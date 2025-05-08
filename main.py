from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt
import pandas as pd

colores = {"setosa":"red","versicolor":"green","virginica":"blue"}
iris = load_iris()
modelo = KNeighborsClassifier(n_neighbors=1)


df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df["target"] = iris.target
df["target_name"] = df["target"].apply(lambda i: iris.target_names[i])
df["target_name"].value_counts()
print(df.head(5))
print(df["target_name"].value_counts())
print(df["target_name"].describe())
X = df[iris.feature_names]
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)
# Calculamos la precisión
precision = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {precision:.2f}")
for real, pred in zip(y_test, y_pred):
    print(f"Real: {iris.target_names[real]}, Predicho: {iris.target_names[pred]}")

for especie in df["target_name"].unique():
    subset = df[df["target_name"] == especie]
    plt.scatter(subset["petal length (cm)"], subset["petal width (cm)"], label=especie, color=colores[especie])
plt.xlabel("largo del petalo en cm")
plt.ylabel("ancho del petalo en cm")
plt.title("Grafico de petalos")
plt.show()

