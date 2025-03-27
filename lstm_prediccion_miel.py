
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# ===================== Cargar y preparar datos =====================

# Simulación de dataset (reemplazar por datos reales)
# Columnas: ET, RH, HT, HH, WS, HW (producción)
data = pd.read_csv("dataset_miel.csv")

# Variables de entrada y salida
X = data[['ET', 'RH', 'HT', 'HH', 'WS']]
y = data['HW']

# Normalización
scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()
X_scaled = scaler_x.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))

# Convertir a series temporales (ventanas de 7 días)
def create_sequences(X, y, time_steps=7):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        Xs.append(X[i:i + time_steps])
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)

X_seq, y_seq = create_sequences(X_scaled, y_scaled)

# Dividir en entrenamiento/prueba
split = int(0.8 * len(X_seq))
X_train, X_test = X_seq[:split], X_seq[split:]
y_train, y_test = y_seq[:split], y_seq[split:]

# ===================== Modelo LSTM =====================

model = Sequential([
    LSTM(256, activation='relu', return_sequences=True, input_shape=(X_seq.shape[1], X_seq.shape[2])),
    BatchNormalization(),
    Dropout(0.3),

    LSTM(128, activation='relu', return_sequences=True),
    BatchNormalization(),
    Dropout(0.3),

    LSTM(64, activation='relu'),
    BatchNormalization(),
    Dropout(0.3),

    Dense(64, activation='relu'),
    Dense(1)  # salida continua (producción de miel)
])

model.compile(optimizer='adam', loss='mse')

# Callbacks
early_stop = EarlyStopping(patience=30, restore_best_weights=True)
lr_schedule = ReduceLROnPlateau(factor=0.5, patience=10)

# ===================== Entrenamiento =====================

history = model.fit(
    X_train, y_train,
    validation_split=0.1,
    epochs=100,
    batch_size=32,
    callbacks=[early_stop, lr_schedule],
    verbose=1
)

# ===================== Evaluación =====================

y_pred_scaled = model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred_scaled)
y_real = scaler_y.inverse_transform(y_test)

r2 = r2_score(y_real, y_pred)
mae = mean_absolute_error(y_real, y_pred)
rmse = np.sqrt(mean_squared_error(y_real, y_pred))

print(f"R2 Score: {r2:.3f}")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")

# ===================== Visualización =====================

plt.figure(figsize=(10, 4))
plt.plot(y_real, label='Real')
plt.plot(y_pred, label='Predicho')
plt.title("Predicción de Producción de Miel (LSTM)")
plt.xlabel("Días")
plt.ylabel("Producción (kg)")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
