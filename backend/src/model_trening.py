"""
CPVClassifier Training Module
Model: CPVClassifier (Random Forest Classifier)
Projekt: BidInsight - Automatyczna kategoryzacja ofert przetargowych
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# Konfiguracja
RANDOM_STATE = 42
TEST_SIZE = 0.2
N_JOBS = -1  # Wykorzystanie wszystkich dostępnych rdzeni


def load_data(file_path):
    """
    Wczytuje dane z pliku CSV.
    
    Parameters:
    -----------
    file_path : str
        Ścieżka do pliku CSV z danymi
        
    Returns:
    --------
    pd.DataFrame
        Wczytane dane
    """
    print(f"Wczytuję dane z {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Wczytano {len(df)} rekordów")
    return df


def prepare_features_target(df, cpv_col='CPV', feature_cols=None):
    """
    Przygotowuje cechy (X) i target (y) z danych.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame z danymi
    cpv_col : str
        Nazwa kolumny z kodem CPV (target)
    feature_cols : list
        Lista kolumn do użycia jako cechy (None = wszystkie oprócz cpv_col)
        
    Returns:
    --------
    tuple
        (X, y) - cechy i target
    """
    if feature_cols is None:
        feature_cols = [col for col in df.columns if col != cpv_col]
    
    X = df[feature_cols]
    y = df[cpv_col]
    
    print(f"Liczba cech: {X.shape[1]}")
    print(f"Liczba kategorii CPV: {y.nunique()}")
    
    return X, y


def encode_target(y):
    """
    Koduje target (kody CPV) do wartości numerycznych.
    
    Parameters:
    -----------
    y : pd.Series
        Target (kody CPV)
        
    Returns:
    --------
    tuple
        (y_encoded, label_encoder) - zakodowany target i encoder
    """
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    print(f"Zakodowano {len(label_encoder.classes_)} kategorii CPV")
    
    return y_encoded, label_encoder


def train_random_forest(X_train, y_train, n_estimators=100, max_depth=None, 
                        min_samples_split=2, min_samples_leaf=1, 
                        random_state=RANDOM_STATE, n_jobs=N_JOBS):
    """
    Trenuje model Random Forest.
    
    Parameters:
    -----------
    X_train : pd.DataFrame lub np.array
        Cechy treningowe
    y_train : np.array
        Target treningowy
    n_estimators : int
        Liczba drzew w lesie
    max_depth : int lub None
        Maksymalna głębokość drzew
    min_samples_split : int
        Minimalna liczba próbek do podziału węzła
    min_samples_leaf : int
        Minimalna liczba próbek w liściu
    random_state : int
        Seed dla reprodukowalności
    n_jobs : int
        Liczba równoległych zadań
        
    Returns:
    --------
    RandomForestClassifier
        Wytrenowany model
    """
    print("Trenuję model Random Forest...")
    print(f"Parametry: n_estimators={n_estimators}, max_depth={max_depth}")
    
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        random_state=random_state,
        n_jobs=n_jobs,
        verbose=1
    )
    
    model.fit(X_train, y_train)
    print("Trening zakończony!")
    
    return model


def evaluate_model(model, X_test, y_test, label_encoder):
    """
    Ewaluuje model na zbiorze testowym.
    
    Parameters:
    -----------
    model : RandomForestClassifier
        Wytrenowany model
    X_test : pd.DataFrame lub np.array
        Cechy testowe
    y_test : np.array
        Target testowy (zakodowany)
    label_encoder : LabelEncoder
        Encoder do dekodowania kodów CPV
        
    Returns:
    --------
    dict
        Słownik z metrykami
    """
    print("\n" + "="*50)
    print("EWALUACJA MODELU")
    print("="*50)
    
    # Predykcje
    y_pred = model.predict(X_test)
    
    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, 
                                target_names=label_encoder.classes_))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # Metryki
    metrics = {
        'accuracy': accuracy,
        'classification_report': classification_report(y_test, y_pred, 
                                                         target_names=label_encoder.classes_,
                                                         output_dict=True),
        'confusion_matrix': cm
    }
    
    return metrics


def plot_confusion_matrix(cm, label_encoder, save_path=None):
    """
    Wizualizuje macierz pomyłek.
    
    Parameters:
    -----------
    cm : np.array
        Macierz pomyłek
    label_encoder : LabelEncoder
        Encoder do dekodowania kodów CPV
    save_path : str
        Ścieżka do zapisania wykresu (None = nie zapisuj)
    """
    plt.figure(figsize=(14, 12))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=label_encoder.classes_,
                yticklabels=label_encoder.classes_)
    plt.xlabel('Predykcja')
    plt.ylabel('Rzeczywistość')
    plt.title('Macierz pomyłek')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_feature_importance(model, feature_names, top_n=20, save_path=None):
    """
    Wizualizuje ważność cech.
    
    Parameters:
    -----------
    model : RandomForestClassifier
        Wytrenowany model
    feature_names : list
        Nazwy cech
    top_n : int
        Liczba top cech do wyświetlenia
    save_path : str
        Ścieżka do zapisania wykresu (None = nie zapisuj)
    """
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    
    plt.figure(figsize=(12, 8))
    plt.barh(range(top_n), importances[indices])
    plt.yticks(range(top_n), [feature_names[i] for i in indices])
    plt.xlabel('Ważność cechy')
    plt.title(f'Top {top_n} najważniejszych cech')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def save_model(model, label_encoder, file_path):
    """
    Zapisuje model i encoder do pliku.
    
    Parameters:
    -----------
    model : RandomForestClassifier
        Wytrenowany model
    label_encoder : LabelEncoder
        Encoder do dekodowania kodów CPV
    file_path : str
        Ścieżka do zapisania modelu
    """
    model_data = {
        'model': model,
        'label_encoder': label_encoder
    }
    
    with open(file_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"Model zapisany do {file_path}")


def load_model(file_path):
    """
    Wczytuje model i encoder z pliku.
    
    Parameters:
    -----------
    file_path : str
        Ścieżka do pliku z modelem
        
    Returns:
    --------
    tuple
        (model, label_encoder)
    """
    with open(file_path, 'rb') as f:
        model_data = pickle.load(f)
    
    return model_data['model'], model_data['label_encoder']


def grid_search_cv(X_train, y_train, param_grid=None, cv=5):
    """
    Wykonuje Grid Search z walidacją krzyżową.
    
    Parameters:
    -----------
    X_train : pd.DataFrame lub np.array
        Cechy treningowe
    y_train : np.array
        Target treningowy
    param_grid : dict
        Siatka parametrów do przeszukania
    cv : int
        Liczba foldów w walidacji krzyżowej
        
    Returns:
    --------
    GridSearchCV
        Obiekt GridSearchCV z najlepszym modelem
    """
    if param_grid is None:
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5, 10]
        }
    
    print("Rozpoczynam Grid Search...")
    print(f"Parametry do przeszukania: {param_grid}")
    
    model = RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=N_JOBS)
    grid_search = GridSearchCV(
        model, param_grid, cv=cv, scoring='accuracy', 
        n_jobs=N_JOBS, verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"\nNajlepsze parametry: {grid_search.best_params_}")
    print(f"Najlepszy score: {grid_search.best_score_:.4f}")
    
    return grid_search


def main():
    """
    Główna funkcja - przykład użycia.
    """
    # Wczytanie danych
    # UZUPEŁNIJ ŚCIEŻKĘ DO DANYCH
    # df = load_data('dane/prepared_data.csv')
    
    # Przygotowanie cech i targetu
    # X, y = prepare_features_target(df)
    
    # Kodowanie targetu
    # y_encoded, label_encoder = encode_target(y)
    
    # Podział danych
    # X_train, X_test, y_train, y_test = train_test_split(
    #     X, y_encoded, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_encoded
    # )
    
    # Trening modelu
    # model = train_random_forest(X_train, y_train, n_estimators=100)
    
    # Ewaluacja
    # metrics = evaluate_model(model, X_test, y_test, label_encoder)
    
    # Wizualizacje
    # plot_confusion_matrix(metrics['confusion_matrix'], label_encoder, 
    #                       save_path='wizualizacje/confusion_matrix.png')
    # plot_feature_importance(model, X.columns.tolist(), 
    #                        save_path='wizualizacje/feature_importance.png')
    
    # Zapis modelu
    # save_model(model, label_encoder, 'modele/random_forest_model.pkl')
    
    print("Uzupełnij kod w funkcji main() z właściwymi ścieżkami i danymi")


if __name__ == "__main__":
    main()


