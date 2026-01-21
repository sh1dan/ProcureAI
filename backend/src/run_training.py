"""
CPVClassifier Training Script
Model: CPVClassifier (Random Forest Classifier)
Projekt: BidInsight - Automatyczna kategoryzacja ofert przetargowych
"""

import sys
from pathlib import Path
import csv
import pickle
from collections import Counter

# Sprawdzenie zależności sklearn
try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report
except ImportError as e:
    print("=" * 60)
    print("BLAD: Brakuje wymaganych bibliotek!")
    print("=" * 60)
    print("Zainstaluj wymagane biblioteki:")
    print("  pip install numpy scikit-learn")
    print("\nLub uzyj Google Colab, gdzie biblioteki sa juz zainstalowane.")
    sys.exit(1)

# Konfiguracja
RANDOM_STATE = 42
DATA_PATH = Path(__file__).parent.parent / 'data' / 'ted_sample.csv'
BASE_DIR = Path(__file__).parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'model.pkl'
TEST_SIZE = 0.2

def load_data(file_path):
    """Wczytuje dane z CSV."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def prepare_features(data):
    """Przygotowuje cechy z danych."""
    # Unikalne wartości dla kodowania
    cae_names = sorted(set(row['CAE_NAME'] for row in data))
    nuts_codes = sorted(set(row['NUTS'] for row in data))
    contract_types = sorted(set(row['TYPE_OF_CONTRACT'] for row in data))
    
    # Mapowanie do indeksów
    cae_map = {name: i for i, name in enumerate(cae_names)}
    nuts_map = {code: i for i, code in enumerate(nuts_codes)}
    contract_map = {ct: i for i, ct in enumerate(contract_types)}
    
    X = []
    y = []
    
    for row in data:
        # Cecha numeryczna: VALUE_EURO (znormalizowana)
        value = float(row['VALUE_EURO'])
        
        # Cechy kategoryczne: one-hot encoding
        cae_idx = cae_map[row['CAE_NAME']]
        nuts_idx = nuts_map[row['NUTS']]
        contract_idx = contract_map[row['TYPE_OF_CONTRACT']]
        
        # Tworzenie wektora cech
        features = [value]
        
        # One-hot encoding dla CAE_NAME
        cae_onehot = [0] * len(cae_names)
        cae_onehot[cae_idx] = 1
        features.extend(cae_onehot)
        
        # One-hot encoding dla NUTS
        nuts_onehot = [0] * len(nuts_codes)
        nuts_onehot[nuts_idx] = 1
        features.extend(nuts_onehot)
        
        # One-hot encoding dla TYPE_OF_CONTRACT
        contract_onehot = [0] * len(contract_types)
        contract_onehot[contract_idx] = 1
        features.extend(contract_onehot)
        
        X.append(features)
        y.append(int(row['CPV']))
    
    X = np.array(X)
    y = np.array(y)
    
    # Normalizacja VALUE_EURO
    scaler = StandardScaler()
    X[:, 0:1] = scaler.fit_transform(X[:, 0:1])
    
    return X, y, scaler, cae_names, nuts_codes, contract_types

def main():
    """Główna funkcja treningu modelu."""
    print("=" * 60)
    print("TRENING MODELU RANDOM FOREST - PROJEKT BIDINSIGHT")
    print("=" * 60)
    
    # 1. Wczytanie danych
    print("\n1. Wczytanie danych...")
    data = load_data(DATA_PATH)
    print(f"   Wczytano {len(data)} rekordow")
    
    # 2. Przygotowanie cech
    print("\n2. Przygotowanie cech...")
    X, y, scaler, cae_names, nuts_codes, contract_types = prepare_features(data)
    print(f"   Liczba cech: {X.shape[1]}")
    print(f"   Liczba kategorii CPV: {len(np.unique(y))}")
    
    # 3. Kodowanie targetu
    print("\n3. Kodowanie targetu...")
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    print(f"   Zakodowano {len(label_encoder.classes_)} kategorii CPV")
    
    # 4. Podzial danych
    print("\n4. Podzial danych (train/test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y_encoded
    )
    print(f"   Zbior treningowy: {X_train.shape[0]} rekordow")
    print(f"   Zbior testowy: {X_test.shape[0]} rekordow")
    
    # 5. Trening modelu
    print("\n5. Trening modelu Random Forest...")
    print("   Parametry: n_estimators=100, max_depth=None")
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbose=0
    )
    
    model.fit(X_train, y_train)
    print("   Trening zakonczony!")
    
    # 6. Ewaluacja modelu
    print("\n6. Ewaluacja modelu...")
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    f1_weighted = f1_score(y_test, y_pred, average='weighted')
    precision_macro = precision_score(y_test, y_pred, average='macro')
    precision_weighted = precision_score(y_test, y_pred, average='weighted')
    recall_macro = recall_score(y_test, y_pred, average='macro')
    recall_weighted = recall_score(y_test, y_pred, average='weighted')
    
    print("\n" + "=" * 60)
    print("EWALUACJA MODELU")
    print("=" * 60)
    print(f"\nAccuracy:           {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"F1-Score (macro):    {f1_macro:.4f}")
    print(f"F1-Score (weighted): {f1_weighted:.4f}")
    print(f"Precision (macro):   {precision_macro:.4f}")
    print(f"Precision (weighted): {precision_weighted:.4f}")
    print(f"Recall (macro):      {recall_macro:.4f}")
    print(f"Recall (weighted):   {recall_weighted:.4f}")
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, 
                                target_names=[str(c) for c in label_encoder.classes_]))
    
    # 7. Zapis modelu
    print("\n7. Zapis modelu...")
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    model_data = {
        'model': model,
        'label_encoder': label_encoder,
        'scaler': scaler,
        'cae_names': cae_names,
        'nuts_codes': nuts_codes,
        'contract_types': contract_types
    }
    
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"   Model zapisany do: {MODEL_PATH}")
    
    # 8. Zapis metryk
    metrics_file = MODEL_PATH.parent / 'metrics.txt'
    with open(metrics_file, 'w', encoding='utf-8') as f:
        f.write("METRYKI MODELU RANDOM FOREST\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Accuracy:           {accuracy:.4f} ({accuracy*100:.2f}%)\n")
        f.write(f"F1-Score (macro):    {f1_macro:.4f}\n")
        f.write(f"F1-Score (weighted): {f1_weighted:.4f}\n")
        f.write(f"Precision (macro):   {precision_macro:.4f}\n")
        f.write(f"Precision (weighted): {precision_weighted:.4f}\n")
        f.write(f"Recall (macro):      {recall_macro:.4f}\n")
        f.write(f"Recall (weighted):   {recall_weighted:.4f}\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write("CLASSIFICATION REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write(classification_report(y_test, y_pred,
                                     target_names=[str(c) for c in label_encoder.classes_]))
    
    print(f"   Metryki zapisane do: {metrics_file}")
    
    # 9. Waznosc cech
    print("\n8. Analiza waznosci cech...")
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:20]
    
    feature_names = ['VALUE_EURO'] + \
                    [f'CAE_NAME_{name}' for name in cae_names] + \
                    [f'NUTS_{code}' for code in nuts_codes] + \
                    [f'TYPE_{ct}' for ct in contract_types]
    
    print("\nTop 20 najwazniejszych cech:")
    for i, idx in enumerate(indices[:20], 1):
        print(f"   {i:2d}. {feature_names[idx]:40s} {importances[idx]:.6f}")
    
    print("\n" + "=" * 60)
    print("TRENING ZAKONCZONY POMYSLNIE!")
    print("=" * 60)
    print(f"\nModel zapisany w: {MODEL_PATH}")
    print(f"Metryki zapisane w: {metrics_file}")
    
    return {
        'model': model,
        'label_encoder': label_encoder,
        'accuracy': accuracy,
        'f1_macro': f1_macro,
        'f1_weighted': f1_weighted,
        'precision_macro': precision_macro,
        'precision_weighted': precision_weighted,
        'recall_macro': recall_macro,
        'recall_weighted': recall_weighted,
        'classification_report': classification_report(y_test, y_pred,
                                                       target_names=[str(c) for c in label_encoder.classes_],
                                                       output_dict=True)
    }

if __name__ == "__main__":
    results = main()

