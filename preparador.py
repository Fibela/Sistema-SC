import os
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split, RandomizedSearchCV, KFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score
import numpy as np
from scikeras.wrappers import KerasClassifier
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from scipy.stats import uniform
from scipy.sparse import csr_matrix

# Configurar early stopping y checkpoints
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
checkpoint = ModelCheckpoint(filepath='best_model.h5', monitor='val_loss', save_best_only=True, verbose=1)

# Desactivar optimizaciones de oneDNN
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Cargar el archivo CSV
df = pd.read_csv('clasificacion.csv')

# Mostrar información básica del DataFrame
print(df.info())
print(df.head())

# Contar la longitud total de caracteres en las primeras filas
total_caracteres = df.head(2).astype(str).applymap(len).sum().sum()
print(f"Total de caracteres en las primeras 2 filas: {total_caracteres}")

# Verificar si hay valores nulos
print(df.isnull().sum())

# Eliminar filas con valores nulos (opcional, dependiendo del contexto)
df = df.dropna()

# Definir características y etiqueta
X = df.drop(columns=['nivel'])  # Características
y = df['nivel']  # Etiqueta (variable objetivo)

# Ver los valores únicos en la columna 'nivel'
print(y.unique())

# Identificar columnas numéricas y categóricas
num_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_features = X.select_dtypes(include=(['object'])).columns.tolist()

# Verificar las columnas numéricas y categóricas
print(f"Columnas numéricas: {num_features}")
print(f"Columnas categóricas: {cat_features}")

# Crear transformador para las columnas categóricas y numéricas usando los nombres de las columnas
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(with_mean=False), num_features),  # Pasar with_mean=False
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
    ], sparse_threshold=0)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Ajustar el preprocesador y transformar los datos
X_train = preprocessor.fit_transform(X_train)
X_test = preprocessor.transform(X_test)

# Convertir matrices dispersas a formato denso
X_train = X_train.toarray() if isinstance(X_train, csr_matrix) else X_train
X_test = X_test.toarray() if isinstance(X_test, csr_matrix) else X_test

# Verificar la forma de X_train después de la transformación
print(f"Shape de X_train después de la transformación: {X_train.shape}")
print(f"Shape de X_test después de la transformación: {X_test.shape}")

# Definir input_shape basado en la forma transformada
input_shape = X_train.shape[1]
print(f"input_shape: {input_shape}")

# Mostrar el número de clases únicas en la columna 'nivel'
num_clases = len(y.unique())
print(f'Número de clases: {num_clases}')

# Codificar 'y' como una matriz 'one-hot'
y_train = to_categorical(y_train, num_classes=num_clases)
y_test = to_categorical(y_test, num_classes=num_clases)

# Definir la función para crear el modelo
def create_model(neurons=128, dropout_rate=0.433, learning_rate=0.00027):
    model = Sequential([
        Input(shape=(input_shape,)),
        Dense(neurons, activation='relu'),
        Dropout(dropout_rate),
        Dense(neurons, activation='relu'),
        Dense(num_clases, activation='softmax')
    ])
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Crear el KerasClassifier con los parámetros por defecto
model = KerasClassifier(
    model=create_model,
    epochs=100,
    batch_size=32,
    verbose=0
)

# Definir los parámetros para el RandomizedSearchCV
param_dist = {
    'model__neurons': [32, 64, 128],
    'model__dropout_rate': uniform(0.3, 0.2),
    'model__learning_rate': uniform(0.00001, 0.0005),  # Rango reducido
    'batch_size': [16, 32, 64],
    'epochs': [20, 50]  # Número de épocas reducido
}

# Crear fit_params para pasar callbacks
fit_params = {
    'callbacks': [early_stopping, checkpoint]
}

# Realizar la búsqueda de hiperparámetros directamente en los datos transformados
random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist, n_iter=10, n_jobs=-1, cv=3, verbose=2)
random_search.fit(X_train, y_train, **fit_params)

# Mostrar los mejores parámetros y resultados
print(f"Mejores Parámetros: {random_search.best_params_}")
print(f"Mejor Score: {random_search.best_score_}")

# Evaluar el rendimiento del modelo con los mejores parámetros en el conjunto de prueba
best_model = random_search.best_estimator_
loss, accuracy = best_model.model_.evaluate(X_test, y_test, verbose=0)
print(f'Pérdida: {loss}, Precisión: {accuracy}')

# Implementar Validación Cruzada
kf = KFold(n_splits=5, shuffle=True, random_state=42)
accuracies = []

for train_index, val_index in kf.split(X_train):
    X_fold_train, X_fold_val = X_train[train_index], X_train[val_index]
    y_fold_train, y_fold_val = y_train[train_index], y_train[val_index]

    # Crear y entrenar el modelo
    model = create_model(neurons=random_search.best_params_['model__neurons'],
                         dropout_rate=random_search.best_params_['model__dropout_rate'],
                         learning_rate=random_search.best_params_['model__learning_rate'])
    
    model.fit(X_fold_train, y_fold_train, epochs=random_search.best_params_['epochs'], batch_size=random_search.best_params_['batch_size'], verbose=0)
    
    # Evaluar el modelo en el fold de validación
    y_pred = model.predict(X_fold_val)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true_classes = np.argmax(y_fold_val, axis=1)
    accuracy = accuracy_score(y_true_classes, y_pred_classes)
    accuracies.append(accuracy)

# Calcular la precisión promedio de la validación cruzada
mean_accuracy = np.mean(accuracies)
print(f'Precisión promedio en la validación cruzada: {mean_accuracy}')
