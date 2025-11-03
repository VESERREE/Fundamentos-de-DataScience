import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import (
    confusion_matrix,
    roc_curve,
    auc,
    precision_recall_curve,
)
    
# Graficar Red_Neuronal.py
def graficar_red_neuronal(y_real, y_pred, titulo="Red Neuronal MLP: Índice de Envejecimiento"):
    # Calcular métricas
    mae = mean_absolute_error(y_real, y_pred)
    mse = mean_squared_error(y_real, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_real, y_pred)

    # Crear figura
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(titulo, fontsize=14, fontweight='bold')

    # === Gráfico 1: Valores Reales vs Predichos ===
    axes[0].scatter(y_real, y_pred, color="#007acc", edgecolor="k", alpha=0.7)
    axes[0].plot([y_real.min(), y_real.max()], [y_real.min(), y_real.max()], 'r--', lw=2, label="Predicción ideal")
    axes[0].set_title("Valores Reales vs Predichos", fontsize=12)
    axes[0].set_xlabel("Valor Real")
    axes[0].set_ylabel("Valor Predicho")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # === Gráfico 2: Distribución de errores ===
    errores = y_pred - y_real
    axes[1].hist(errores, bins=15, color="#ff9800", edgecolor="black", alpha=0.8)
    axes[1].axvline(0, color="red", linestyle="--", linewidth=2, label="Error = 0")
    axes[1].set_title("Distribución de Errores", fontsize=12)
    axes[1].set_xlabel("Error (Predicho - Real)")
    axes[1].set_ylabel("Frecuencia")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # === Mostrar métricas en texto ===
    texto_metricas = (
        f"MAE  = {mae:.2f}\n"
        f"RMSE = {rmse:.2f}\n"
        f"R²    = {r2:.3f}"
    )
    plt.figtext(0.77, 0.25, texto_metricas, fontsize=11, 
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))

    plt.tight_layout()
    plt.show()
    
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

def graficar_arbol_decision(modelo, feature_names, class_names, titulo="Árbol de Decisión"):
    # Limpieza de nombres de variables
    feature_names = [
        nombre.replace("FEATURE_", "")
              .replace("_", " ")
              .title()
        for nombre in feature_names
    ]
    
    # Limpieza de nombres de clases
    class_names = [nombre.replace("_", " ").title() for nombre in class_names]

    # Gráfico
    plt.figure(figsize=(20, 12))
    plot_tree(
        modelo,
        feature_names=feature_names,
        class_names=class_names,
        filled=True,
        rounded=True,
        fontsize=9
    )
    plt.title(titulo, fontsize=16, weight='bold')
    plt.show()


# Graficar Modelo_KNN.py
def graficar_modelo_knn(y_true, y_pred, y_prob=None, titulo="Rendimiento del Modelo de Clasificación"):
    """
    Grafica la matriz de confusión, curva ROC y curva Precisión-Recall
    para cualquier modelo de clasificación binaria.

    Parámetros:
    - y_true: etiquetas reales
    - y_pred: etiquetas predichas (0 o 1)
    - y_prob: probabilidades predichas (opcional, para curvas ROC/PR)
    - titulo: título general del gráfico
    """
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))

    # === 1. Matriz de confusión ===
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[0])
    axes[0].set_title("Matriz de Confusión", fontsize=14)
    axes[0].set_xlabel("Predicción")
    axes[0].set_ylabel("Real")
    axes[0].set_xticklabels(["Bajo Riesgo", "Alto Riesgo"])
    axes[0].set_yticklabels(["Bajo Riesgo", "Alto Riesgo"], rotation=0)

    # === 2. Curva ROC ===
    if y_prob is not None:
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        roc_auc = auc(fpr, tpr)
        axes[1].plot(fpr, tpr, color="darkorange", lw=2, label=f"AUC = {roc_auc:.2f}")
        axes[1].plot([0, 1], [0, 1], color="gray", linestyle="--")
        axes[1].set_xlim([0.0, 1.0])
        axes[1].set_ylim([0.0, 1.05])
        axes[1].set_title("Curva ROC", fontsize=14)
        axes[1].set_xlabel("False Positive Rate")
        axes[1].set_ylabel("True Positive Rate")
        axes[1].legend(loc="lower right")

    # === 3. Curva Precisión-Recall ===
    if y_prob is not None:
        precision, recall, _ = precision_recall_curve(y_true, y_prob)
        axes[2].plot(recall, precision, color="purple", lw=2)
        axes[2].set_xlim([0.0, 1.0])
        axes[2].set_ylim([0.0, 1.05])
        axes[2].set_title("Curva Precisión-Recall", fontsize=14)
        axes[2].set_xlabel("Recall")
        axes[2].set_ylabel("Precisión")

    fig.suptitle(titulo, fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.show()
    
def graficar_regresion_lineal(df, x_col, y_col, titulo="Relación entre variables (Regresión Lineal)"):
    plt.figure(figsize=(8, 5))
    sns.set(style="whitegrid")

    # Gráfico de dispersión + línea de regresión
    sns.regplot(
        x=x_col, 
        y=y_col, 
        data=df, 
        ci=None, 
        scatter_kws={'color': 'skyblue', 'alpha': 0.7}, 
        line_kws={'color': 'red', 'linewidth': 2}
    )

    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.xlabel(x_col, fontsize=12)
    plt.ylabel(y_col, fontsize=12)
    plt.tight_layout()
    plt.show()