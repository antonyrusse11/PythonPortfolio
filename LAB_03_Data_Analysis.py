import numpy as np
import pandas as pd

# Load data and get column names
df = pd.read_csv("poisson-data.csv")

# --- FIX: Rename the columns explicitly for clean printing ---
df.columns = ['Data Set 1', 'Data Set 2']

# Use the new, clean column names
column_1_name = df.columns[0] 
column_2_name = df.columns[1] 

data_1 = df[column_1_name]
data_2 = df[column_2_name]

# --- Calculations (Unchanged) ---
mean_1 = np.mean(data_1)
std_dev_1 = np.std(data_1, ddof=0)
std_err_1 = std_dev_1 / np.sqrt(len(data_1)) 
sqrt_mean_1 = np.sqrt(mean_1)

mean_2 = np.mean(data_2)
std_dev_2 = np.std(data_2, ddof=0)
std_err_2 = std_dev_2 / np.sqrt(len(data_2))
sqrt_mean_2 = np.sqrt(mean_2)

# --- Display Results (Now using clean names) ---
print(f"--- Results for Data Set: {column_1_name} ---")
print(f"Mean:                 {mean_1:.4f}")
print(f"Standard Deviation:   {std_dev_1:.4f}")
print(f"Standard Error (SE):  {std_err_1:.4f}")
print(f"Square Root of Mean:  {sqrt_mean_1:.4f}")
print("\n")
print(f"--- Results for Data Set: {column_2_name} ---")
print(f"Mean:                 {mean_2:.4f}")
print(f"Standard Deviation:   {std_dev_2:.4f}")
print(f"Standard Error (SE):  {std_err_2:.4f}")
print(f"Square Root of Mean:  {sqrt_mean_2:.4f}")
