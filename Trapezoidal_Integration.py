# =====================================================================
# IMPORT ESSENTIAL LIBRARIES
# =====================================================================
import math

# =====================================================================
# A. CORE FUNCTION: TRAPEZOIDAL RULE LOGIC
# =====================================================================

def trapezoidal_rule(f, a, b, N):
    
    if a == b: return 0.0

    h = (b - a) / N
    integral_sum = f(a) + f(b)

    # Add twice the sum of the intermediate points
    for i in range(1, N):
        x_i = a + i * h
        integral_sum += 2 * f(x_i)

    # Final calculation and return
    integral = integral_sum * (h / 2)
    return integral
    
# =====================================================================
# B. FIVE FUNCTIONS TO INTEGRATE 
# =====================================================================

def f_task1_poly(x):
    """Function for Task 1: Integrates x^3 + 2."""
    return x**3 + 2

def f_task2_trig_cos(x):
    """Function for Task 2: Integrates cos(x)."""
    return math.cos(x)

def f_task3_exponential(x):
    """Function for Task 3: Integrates 4e^-x."""
    return 4 * math.exp(-x)

def f_task4_rational(x):
    """Function for Task 4: Integrates 1/(1+x^2)."""
    return 1 / (1 + x**2) 

def f_task5_linear(x):
    """Function for Task 5: Integrates 3x + 1."""
    return 3 * x + 1

# =====================================================================
# C. SINGLE EXECUTION BLOCK (ALL TASKS CONSOLIDATED)
# =====================================================================

def execute_task(task_num, f_func, a, b, N, f_str, exact_val):
    """Helper function to run the trapezoidal rule and print formatted output."""
    result = trapezoidal_rule(f_func, a, b, N)
    
    print(f"\n==================================================")
    print(f"--- TASK {task_num}/5: NUMERICAL INTEGRATION ---")
    print(f"Function: {f_str}")
    print(f"Interval: [{a}, {b}]")
    print(f"Intervals (N): {N}")
    print(f"Approximated Integral: {result:.8f}")
    
    if exact_val is not None:
        error = abs(result - exact_val)
        print(f"Exact Value: {exact_val:.8f}")
        print(f"Absolute Error: {error:.8f}")
    print(f"==================================================")

if __name__ == "__main__":
    
    print("--- Laboratory 8 - 2: Numerical Integration by Trapezoidal Rule ---")
    
    # --- TASK 1 Execution ---
    execute_task(
        task_num=1,
        f_func=f_task1_poly,
        a=1.0, b=3.0, N=2,
        f_str="f(x) = x^3 + 2",
        exact_val=24.0 # Exact integral of x^3 + 2 from 1 to 3
    )

    # --- TASK 2 Execution ---
    execute_task(
        task_num=2,
        f_func=f_task2_trig_cos,
        a=0.0, b=math.pi, N=4,
        f_str="f(x) = cos(x)",
        exact_val=0.0 # Integral of cos(x) from 0 to pi
    )

    # --- TASK 3 Execution ---
    execute_task(
        task_num=3,
        f_func=f_task3_exponential,
        a=4, b=8, N=2,
        f_str="f(x) = 4e^-x",
        exact_val=4*math.exp(-4) - 4*math.exp(-8) # Exact integral of 4e^-x from 4 to 8
    )

        # --- TASK 4 Execution ---
    execute_task(
        task_num=4,
        f_func=f_task4_rational,
        a=5, b=11, N=4,
        f_str="f(x) = 1/(1+x^2)",
        exact_val=math.atan(11) - math.atan(5) # Exact integral of 1/(1+x^2) from 5 to 11
    )

            # --- TASK 5 Execution ---
    execute_task(
        task_num=5,
        f_func=f_task5_linear,
        a=7, b=18, N=500,
        f_str="f(x) = 1/(1+x^2)",
        exact_val=847/2 # Exact integral of 3x + 1 from 7 to 18
    )

