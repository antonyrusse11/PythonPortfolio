import math

def trapezoidal_rule(f, a, b, n):
    if a == b: return 0.0
    
    h = (b - a) / n
    # Start with end points
    total = f(a) + f(b)

    # Sum internal nodes
    for i in range(1, n):
        total += 2 * f(a + i * h)

    return total * (h / 2)

# Test cases
tasks = [
    {"id": 1, "f": lambda x: x**3 + 2, "range": (1.0, 3.0), "n": 2, "exact": 24.0},
    {"id": 2, "f": math.cos, "range": (0.0, math.pi), "n": 4, "exact": 0.0},
    {"id": 3, "f": lambda x: 4 * math.exp(-x), "range": (4, 8), "n": 2, "exact": 4*math.exp(-4) - 4*math.exp(-8)},
    {"id": 4, "f": lambda x: 1 / (1 + x**2), "range": (5, 11), "n": 4, "exact": math.atan(11) - math.atan(5)},
    {"id": 5, "f": lambda x: 3 * x + 1, "range": (7, 18), "n": 500, "exact": 423.5}
]

if __name__ == "__main__":
    print("Lab 8-2: Trapezoidal Rule Results")
    print("-" * 40)
    
    for t in tasks:
        a, b = t["range"]
        approx = trapezoidal_rule(t["f"], a, b, t["n"])
        error = abs(approx - t["exact"])
        
        print(f"Task {t['id']}: Result = {approx:.6f} (Error: {error:.2e})")
