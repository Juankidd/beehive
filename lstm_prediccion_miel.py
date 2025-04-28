
import numpy as np  # Import required libraries
import pandas as pd  # Import required libraries
import matplotlib.pyplot as plt  # Import required libraries
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# ===================== Load and prepare data =====================

# Connect to IoT system
# Columns: ET, RH, HT, HH, HH, WS, HW (production)
data = pd.read_csv("dataset_miel.csv")  # Load dataset from CSV file

# Input and output variables
X = data[['ET', 'RH', 'HT', 'HH', 'WS']]  # Select input features
y = data['HW']  # Select target variable (honey production)

# Standardization
scaler_x = MinMaxScaler()  # Initialize MinMaxScaler for inputs
scaler_y = MinMaxScaler()  # Initialize MinMaxScaler for outputs
X_scaled = scaler_x.fit_transform(X)  # Scale input features
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))  # Scale target variable

# Convert to time series (7-day windows)
def create_sequences(X, y, time_steps=7):  # Function to create sequences of data for time-series prediction
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        Xs.append(X[i:i + time_steps])
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)

X_seq, y_seq = create_sequences(X_scaled, y_scaled)  # Create sequences from scaled data

# Divide into training/testing
split = int(0.8 * len(X_seq))  # Define index to split training and testing data
X_train, X_test = X_seq[:split], X_seq[split:]  # Split input sequences into training and testing sets
y_train, y_test = y_seq[:split], y_seq[split:]  # Split output sequences into training and testing sets

# ===================== Modelo LSTM  =====================

model = Sequential([  # Build Sequential LSTM model architecture
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
    Dense(1) # continuous output (honey production)
])

model.compile(optimizer='adam', loss='mse')  # Compile the model with optimizer and loss function

# Callbacks
early_stop = EarlyStopping(patience=30, restore_best_weights=True)  # Setup early stopping callback to prevent overfitting
lr_schedule = ReduceLROnPlateau(factor=0.5, patience=10)  # Setup learning rate scheduler callback

# ===================== Training =====================

history = model.fit(  # Train the LSTM model
    X_train, y_train,
    validation_split=0.1,
    epochs=100,
    batch_size=32,
    callbacks=[early_stop, lr_schedule],
    verbose=1
)

# ===================== Evaluation =====================

y_pred_scaled = model.predict(X_test)  # Predict scaled outputs using the trained model
y_pred = scaler_y.inverse_transform(y_pred_scaled)  # Inverse transform predictions to original scale
y_real = scaler_y.inverse_transform(y_test)  # Inverse transform true labels to original scale

r2 = r2_score(y_real, y_pred)  # Calculate R2 score
mae = mean_absolute_error(y_real, y_pred)  # Calculate Mean Absolute Error (MAE)
rmse = np.sqrt(mean_squared_error(y_real, y_pred))  # Calculate Root Mean Squared Error (RMSE)

print(f"R2 Score: {r2:.3f}")  # Print R2 score result
print(f"MAE: {mae:.2f}")  # Print MAE result
print(f"RMSE: {rmse:.2f}")  # Print RMSE result

# ===================== Visualization =====================

plt.figure(figsize=(10, 4))  # Create a new figure for plotting results
plt.plot(y_real, label='Real')  # Plot actual honey production values
plt.plot(y_pred, label='Predicted')  # Plot predicted honey production values
plt.title("Honey Production Forecasting (LSTM)")  # Set the plot title
plt.xlabel("Days")  # Set x-axis label
plt.ylabel("Production (kg)")  # Set y-axis label
plt.legend()  # Add a legend to the plot
plt.grid()  # Add grid lines to the plot
plt.tight_layout()  # Adjust plot layout to avoid overlap
plt.show()  # Display the plot
