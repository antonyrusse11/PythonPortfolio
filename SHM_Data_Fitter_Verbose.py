# Python SHM Data Fitting 

# =====================================================================
# FILE: SHM_Data_Fitter_Verbose.py
# PROJECT: Freelance Data Analysis Portfolio Example 1/3
# AIM: To demonstrate non-linear least squares regression (curve fitting) 
# on experimental data (Simulated Simple Harmonic Motion).
# REQUIRED LIBRARIES: numpy, matplotlib, scipy.optimize
# =====================================================================

# 1. IMPORT NECESSARY LIBRARIES FOR COMPUTATION AND VISUALIZATION

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math

# ---------------------------------------------------------------------
# --- SECTION 2: DATA GENERATION (Simulating a physical experiment) ---
# ---------------------------------------------------------------------

# Define the true physical parameters for generating clean, ideal data.
T_true = 1.25   # True physical period in seconds
omega_true = 2 * math.pi / T_true # Calculate angular frequency (omega = 2*pi / T)

# Create a time array (the independent variable 't')
t_data = np.linspace(0, 5, 50) # 50 data points collected over 5 seconds

# Generate the ideal, clean Simple Harmonic Motion (SHM) curve.
# SHM Formula: y = A * cos(omega*t + phi) + C
y_true = 5.0 * np.cos(omega_true * t_data + 0.5) + 10.0

# Add random noise to the ideal data to simulate real-world experimental measurement errors.
y_data = y_true + 0.5 * np.random.normal(size=len(t_data)) 

# ---------------------------------------------------------------------
# --- SECTION 3: MATHEMATICAL MODEL DEFINITION ---
# ---------------------------------------------------------------------

def shm_model(t, A, omega, phi, C):
    """
    Defines the general sinusoidal mathematical model used for the non-linear regression.
    This function represents the expected physical behavior of the system.
    
    INPUTS:
    - t (Time): The independent variable array.
    - A (Amplitude): Maximum displacement from equilibrium.
    - omega (Angular Frequency): Rate of oscillation.
    - phi (Phase Angle): Horizontal shift of the wave.
    - C (Vertical Offset): The equilibrium point (mean).
    """
    return A * np.cos(omega * t + phi) + C

# ---------------------------------------------------------------------
# --- SECTION 4: INITIAL PARAMETER GUESSES (CRITICAL FOR OPTIMIZATION) ---
# ---------------------------------------------------------------------

# The non-linear solver requires good initial guesses (p0) to find the optimum fit (popt).
# We estimate these parameters directly from the raw, noisy data to aid convergence.

# A. Vertical Offset (C): Estimated as the mean of all collected data points.
C_guess = np.mean(y_data)

# B. Amplitude (A): Estimated as half of the observed peak-to-peak range.
A_guess = (np.max(y_data) - np.min(y_data)) / 2

# C. Angular Frequency (omega): Estimate based on the true known period (1.25s) from the simulation setup.
T_guess = 1.25 
omega_guess = 2 * math.pi / T_guess

# D. Phase Angle (phi): Usually initialized to zero radians for stability.
phi_guess = 0.0

# Store the initial guesses in the required vector format.
p0 = [A_guess, omega_guess, phi_guess, C_guess] 

print("--- Initializing Solver ---")
print(f"Initial Parameter Guesses (p0): {p0}")
print("-" * 30)

# ---------------------------------------------------------------------
# --- SECTION 5: NON-LINEAR CURVE FITTING (Least Squares Optimization) ---
# ---------------------------------------------------------------------

# The try/except block handles potential RuntimeError if the optimization fails to converge.
try:
    # curve_fit performs the Levenberg-Marquardt algorithm (non-linear least squares).
    popt, pcov = curve_fit(shm_model, t_data, y_data, p0=p0)
    
    # Extract the final optimized parameters (popt)
    A_fit, omega_fit, phi_fit, C_fit = popt
    
    # Calculate derived quantity: The fitted physical period.
    T_fit = 2 * math.pi / omega_fit

except RuntimeError:
    print("\nError: Optimization failed. Check data or adjust initial guesses.")
    # Use initial guess values if the optimization process fails.
    A_fit, omega_fit, phi_fit, C_fit = p0
    T_fit = 2 * math.pi / omega_guess 

# ---------------------------------------------------------------------
# --- SECTION 6: RESULTS OUTPUT AND VISUALIZATION ---
# ---------------------------------------------------------------------

if __name__ == "__main__":
    
    # Print the final, numerically verified parameters in a clear, readable format.
    print("\n--- FINAL FITTED SHM PARAMETERS (Verification) ---")
    print(f"Amplitude (A): {A_fit:.4f}")
    print(f"Angular Frequency (omega): {omega_fit:.4f} rad/s")
    print(f"Period (T) [Derived]: {T_fit:.4f} seconds")
    print(f"Phase Angle (phi): {phi_fit:.4f} radians")
    print(f"Vertical Offset (C) [Equilibrium]: {C_fit:.4f}")
    print("-" * 50)

    # Prepare the final smooth curve for plotting.
    t_fit = np.linspace(min(t_data), max(t_data), 500)
    y_fit = shm_model(t_fit, *popt) 

    plt.figure(figsize=(10, 6))
    
    # Plot 1: Display the original raw data points (the experiment).
    plt.scatter(t_data, y_data, label='Experimental Data (with Noise)', s=20, color='darkgray', alpha=0.8)
    
    # Plot 2: Display the smooth best-fit curve (the theory validated by code).
    plt.plot(t_fit, y_fit, color='red', linewidth=3, label=f'Best Fit Curve (T={T_fit:.2f}s)')
    
    # Add horizontal line showing the calculated equilibrium position (C).
    plt.axhline(C_fit, color='blue', linestyle='--', label=f'Equilibrium Position (C={C_fit:.2f})')
    
    # Final plot formatting for professional presentation.
    plt.title('Laboratory 8-1: Simple Harmonic Motion Data Fitting')
    plt.xlabel('Time (s)')
    plt.ylabel('Displacement (y)')
    plt.legend()
    plt.grid(True)
    plt.show()
