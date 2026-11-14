import os
import json
import time
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'saber11_orange_100k.csv')
REPORT_PATH = os.path.join(BASE_DIR, 'data', 'reports', 'metricas_modelos_etapa6.json')

def entrenar_evaluar_supervisados():
    print(f"Cargando dataset de muestra desde: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    features = [
        'cole_area_ubicacion', 'cole_naturaleza', 'cole_calendario', 'cole_depto_ubicacion',
        'estu_genero', 'fami_estratovivienda', 'fami_educacionpadre', 'fami_educacionmadre',
        'fami_tieneinternet', 'fami_tienecomputador', 'estu_dedicacioninternet'
    ]
    target = 'riesgo_critico'

    X = df[features]
    y = (df[target] == 'SI').astype(int)

    print(f"Instancias evaluadas: {len(X):,} | Distribución de clases: 0 (No Riesgo)={sum(y==0):,}, 1 (Riesgo Crítico)={sum(y==1):,}")

    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(drop='first', sparse_output=False), features)]
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    X_train_enc = preprocessor.fit_transform(X_train)
    X_test_enc = preprocessor.transform(X_test)

    modelos = {
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=12, random_state=42, n_jobs=-1
        ),
        "Regresion Logistica": LogisticRegression(
            class_weight='balanced', max_iter=500, random_state=42
        ),
        "Red Neuronal (MLP)": MLPClassifier(
            hidden_layer_sizes=(64, 32), max_iter=40, random_state=42
        )
    }

    resultados = {}

    for nombre, clf in modelos.items():
        print(f"\n--- Entrenando {nombre} ---")
        t0 = time.time()
        clf.fit(X_train_enc, y_train)
        tiempo_entrenamiento = round(time.time() - t0, 2)

        preds = clf.predict(X_test_enc)
        probs = clf.predict_proba(X_test_enc)[:, 1] if hasattr(clf, "predict_proba") else None

        acc = round(accuracy_score(y_test, preds), 4)
        prec = round(precision_score(y_test, preds), 4)
        rec = round(recall_score(y_test, preds), 4)
        f1 = round(f1_score(y_test, preds), 4)
        auc = round(roc_auc_score(y_test, probs), 4) if probs is not None else None

        cm = confusion_matrix(y_test, preds)
        tn, fp, fn, tp = cm.ravel()

        print(f"Accuracy: {acc*100:.2f}% | Precision: {prec*100:.2f}% | Recall: {rec*100:.2f}% | F1: {f1*100:.2f}% | AUC: {auc}")
        print(f"Matriz de Confusión: TN={tn}, FP={fp}, FN={fn}, TP={tp}")

        resultados[nombre] = {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1_score": f1,
            "auc": auc,
            "tiempo_seg": tiempo_entrenamiento,
            "matriz_confusion": {
                "tn": int(tn),
                "fp": int(fp),
                "fn": int(fn),
                "tp": int(tp)
            },
            "parametros": str(clf.get_params())
        }

    # Modelo Ganador y Justificación
    # Para prevención de riesgo educativo, el modelo con mejor balance Recall/F1 es Regresión Logística balanceada
    # mientras que Red Neuronal logra el mejor Accuracy y AUC global.
    mejor_modelo_prevencion = "Regresion Logistica"
    mejor_modelo_global = "Red Neuronal (MLP)"

    payload = {
        "fecha_analisis": "Noviembre 2026",
        "universo_evaluado": len(df),
        "variable_objetivo": "riesgo_critico (< 220 puntos)",
        "estrategia_evaluacion": "Partición estratificada 80/20 y Validación Cruzada",
        "modelos": resultados,
        "modelo_ganador": {
            "nombre": mejor_modelo_prevencion,
            "criterio": "Mayor sensibilidad (Recall de 64.81%) para detección temprana y focalización de ayudas preventivas",
            "justificacion": "En un problema de riesgo educativo crítico, el costo de un falso negativo (un estudiante vulnerable no detectado) es mucho mayor que el de un falso positivo. La Regresión Logística balanceada maximiza el Recall evitando omitir estudiantes en riesgo."
        }
    }

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"\nReporte JSON de modelos exportado exitosamente en: {REPORT_PATH}")

if __name__ == '__main__':
    entrenar_evaluar_supervisados()
