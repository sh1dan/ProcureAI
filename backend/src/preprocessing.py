"""
CPVClassifier Data Preprocessing Module
Projekt: BidInsight - Automatyczna kategoryzacja ofert przetargowych
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split


class DataPreprocessor:
    """
    Klasa do przetwarzania danych przed modelowaniem.
    """
    
    def __init__(self):
        self.scaler = None
        self.label_encoder = None
        self.tfidf_vectorizer = None
        self.feature_names = None
        
    def fit_transform_numeric(self, X, method='standard'):
        """
        Standaryzuje/normalizuje cechy numeryczne.
        
        Parameters:
        -----------
        X : pd.DataFrame lub np.array
            Cechy numeryczne
        method : str
            Metoda skalowania ('standard', 'minmax', 'robust')
            
        Returns:
        --------
        np.array
            Przetransformowane cechy
        """
        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        elif method == 'robust':
            self.scaler = RobustScaler()
        else:
            raise ValueError(f"Nieznana metoda: {method}")
        
        return self.scaler.fit_transform(X)
    
    def transform_numeric(self, X):
        """
        Transformuje cechy numeryczne używając wcześniej dopasowanego skalera.
        
        Parameters:
        -----------
        X : pd.DataFrame lub np.array
            Cechy numeryczne
            
        Returns:
        --------
        np.array
            Przetransformowane cechy
        """
        if self.scaler is None:
            raise ValueError("Najpierw wywołaj fit_transform_numeric()")
        
        return self.scaler.transform(X)
    
    def encode_categorical(self, y, fit=True):
        """
        Koduje kategoryczne wartości (target).
        
        Parameters:
        -----------
        y : pd.Series lub np.array
            Wartości kategoryczne do zakodowania
        fit : bool
            Czy dopasować encoder (True) czy tylko transformować (False)
            
        Returns:
        --------
        np.array
            Zakodowane wartości
        """
        if fit or self.label_encoder is None:
            self.label_encoder = LabelEncoder()
            return self.label_encoder.fit_transform(y)
        else:
            return self.label_encoder.transform(y)
    
    def decode_categorical(self, y_encoded):
        """
        Dekoduje zakodowane wartości kategoryczne.
        
        Parameters:
        -----------
        y_encoded : np.array
            Zakodowane wartości
            
        Returns:
        --------
        np.array
            Zdekodowane wartości
        """
        if self.label_encoder is None:
            raise ValueError("Najpierw wywołaj encode_categorical() z fit=True")
        
        return self.label_encoder.inverse_transform(y_encoded)
    
    def fit_transform_text(self, texts, method='tfidf', max_features=1000):
        """
        Przetwarza teksty używając TF-IDF lub Count Vectorizer.
        
        Parameters:
        -----------
        texts : list lub pd.Series
            Teksty do przetworzenia
        method : str
            Metoda ('tfidf' lub 'count')
        max_features : int
            Maksymalna liczba cech
            
        Returns:
        --------
        np.array
            Macierz cech tekstowych
        """
        if method == 'tfidf':
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=max_features,
                stop_words='english',
                ngram_range=(1, 2)
            )
        elif method == 'count':
            self.tfidf_vectorizer = CountVectorizer(
                max_features=max_features,
                stop_words='english',
                ngram_range=(1, 2)
            )
        else:
            raise ValueError(f"Nieznana metoda: {method}")
        
        return self.tfidf_vectorizer.fit_transform(texts).toarray()
    
    def transform_text(self, texts):
        """
        Transformuje teksty używając wcześniej dopasowanego vectorizera.
        
        Parameters:
        -----------
        texts : list lub pd.Series
            Teksty do przetworzenia
            
        Returns:
        --------
        np.array
            Macierz cech tekstowych
        """
        if self.tfidf_vectorizer is None:
            raise ValueError("Najpierw wywołaj fit_transform_text()")
        
        return self.tfidf_vectorizer.transform(texts).toarray()
    
    def one_hot_encode(self, df, columns):
        """
        Wykonuje one-hot encoding dla wybranych kolumn.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame z danymi
        columns : list
            Lista kolumn do zakodowania
            
        Returns:
        --------
        pd.DataFrame
            DataFrame z zakodowanymi kolumnami
        """
        return pd.get_dummies(df, columns=columns, prefix=columns)
    
    def create_features(self, df, cpv_col='CPV', value_col=None, 
                       categorical_cols=None, text_cols=None):
        """
        Tworzy macierz cech z różnych typów danych.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame z danymi
        cpv_col : str
            Nazwa kolumny z kodem CPV (target)
        value_col : str
            Nazwa kolumny z wartością kontraktu
        categorical_cols : list
            Lista kolumn kategorycznych
        text_cols : list
            Lista kolumn tekstowych
            
        Returns:
        --------
        tuple
            (X, y, feature_names) - cechy, target, nazwy cech
        """
        features_list = []
        feature_names = []
        
        # Cechy numeryczne
        if value_col and value_col in df.columns:
            values = df[value_col].fillna(0).values.reshape(-1, 1)
            values_scaled = self.fit_transform_numeric(values, method='robust')
            features_list.append(values_scaled)
            feature_names.append(value_col)
        
        # Cechy kategoryczne (one-hot encoding)
        if categorical_cols:
            df_encoded = self.one_hot_encode(df[categorical_cols], categorical_cols)
            features_list.append(df_encoded.values)
            feature_names.extend(df_encoded.columns.tolist())
        
        # Cechy tekstowe (TF-IDF)
        if text_cols:
            for text_col in text_cols:
                if text_col in df.columns:
                    texts = df[text_col].fillna('').astype(str)
                    text_features = self.fit_transform_text(texts, method='tfidf')
                    features_list.append(text_features)
                    feature_names.extend([f"{text_col}_{i}" for i in range(text_features.shape[1])])
        
        # Połączenie wszystkich cech
        X = np.hstack(features_list) if features_list else np.array([])
        y = df[cpv_col].values
        
        self.feature_names = feature_names
        
        return X, y, feature_names
    
    def train_test_split_stratified(self, X, y, test_size=0.2, random_state=42):
        """
        Dzieli dane na zbiór treningowy i testowy z zachowaniem rozkładu klas.
        
        Parameters:
        -----------
        X : np.array
            Cechy
        y : np.array
            Target
        test_size : float
            Proporcja zbioru testowego
        random_state : int
            Seed dla reprodukowalności
            
        Returns:
        --------
        tuple
            (X_train, X_test, y_train, y_test)
        """
        return train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )


def example_usage():
    """
    Przykład użycia klasy DataPreprocessor.
    """
    # Przykład danych
    # df = pd.read_csv('dane/prepared_data.csv')
    
    # Inicjalizacja preprocessora
    preprocessor = DataPreprocessor()
    
    # Tworzenie cech
    # X, y, feature_names = preprocessor.create_features(
    #     df,
    #     cpv_col='CPV',
    #     value_col='VALUE_EURO',
    #     categorical_cols=['CAE_NAME', 'NUTS', 'TYPE_OF_CONTRACT'],
    #     text_cols=['TITLE']  # jeśli dostępne
    # )
    
    # Kodowanie targetu
    # y_encoded = preprocessor.encode_categorical(y, fit=True)
    
    # Podział danych
    # X_train, X_test, y_train, y_test = preprocessor.train_test_split_stratified(
    #     X, y_encoded, test_size=0.2, random_state=42
    # )
    
    print("Uzupełnij kod w funkcji example_usage() z właściwymi danymi")


if __name__ == "__main__":
    example_usage()


