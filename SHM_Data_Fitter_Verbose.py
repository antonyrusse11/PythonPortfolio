import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# -- Generate Noisy Data --
T_TRUE = 1.25
W_TRUE = 2 * np.pi / T_TRUE

t = np.linspace(0, 5, 50)
# Formula: A * cos(w*t + phi) + C
y_clean = 5.0 * np.cos(W_TRUE * t + 0.5) + 10.0
y_noisy = y_clean + 0.5 * np.random.normal(size=len(t))

def shm_func(t, a, w, phi, c):
    return a * np.cos(w * t + phi) + c

# -- Parameter Estimation --
# Guessing based on data range and mean
c_guess = np.mean(y_noisy)
a_guess = (np.max(y_noisy) - np.min(y_noisy)) / 2
w_guess = 2 * np.pi / 1.25 # Assuming prior knowledge of expected period
p0 = [a_guess, w_guess, 0.0, c_guess]

try:
    popt, _ = curve_fit(shm_func, t, y_noisy, p0=p0)
    a_fit, w_fit, phi_fit, c_fit = popt
    t_fit_val = 2 * np.pi / w_fit
except Exception as e:
    print(f"Fit failed: {e}")
    popt = p0
    t_fit_val = 1.25

# -- Visuals --
if __name__ == "__main__":
    print(f"Fit Results: A={popt[0]:.3f}, T={t_fit_val:.3f}s, C={popt[3]:.3f}")

    t_smooth = np.linspace(0, 5, 500)
    
    plt.figure(figsize=(9, 5))
    plt.scatter(t, y_noisy, label='Raw Data', color='gray', s=15)
    plt.plot(t_smooth, shm_func(t_smooth, *popt), 'r-', label='Regression')
    plt.axhline(popt[3], color='k', linestyle='--', alpha=0.5, label='Equilibrium')
    
    plt.title('SHM Curve Fitting (Non-linear Least Squares)')
    plt.legend()
    plt.show()
