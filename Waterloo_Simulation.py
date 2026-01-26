import math 

# --- FLIGHT DYNAMICS PARAMETERS ---
# Initializing time state and step size for numerical stability
T = 0
DT = 0.01 # 10ms step size for balanced integration accuracy
X0, Y0 = 0.0, 50.0 

# Projectile: British 9lb smoothbore (approx 4.08kg, 10.2cm diameter)
M = 4.08    
D = 0.102  
AREA = math.pi * (D/2)**2 
CD = 0.45 # Standard drag coefficient for a sphere at subsonic speeds
G = 9.81  
RHO = 1.225 # Constant sea-level air density
V0 = 450.0  
WIND_X, WIND_Y = 5.0, -1.0 # Local atmospheric vectors

ANGLE_DEG = 10.0
RADS = math.radians(ANGLE_DEG)

# State Vector representation: [x, y, vx, vy]
S = [X0, Y0, V0 * math.cos(RADS), V0 * math.sin(RADS)]

def get_rates(state):
    """
    Calculates the derivative of the state vector.
    Solves for instantaneous acceleration including aerodynamic drag and gravity.
    """
    x, y, vx, vy = state

    # Computing relative velocity vector for aerodynamic drag force
    vx_rel = vx - WIND_X 
    vy_rel = vy - WIND_Y 
    v_mag = math.sqrt(vx_rel**2 + vy_rel**2)

    if v_mag == 0:
        drag_f = 0.0
    else:
        # Applying the quadratic drag model (Fd = 0.5 * rho * v^2 * Cd * A)
        # Resulting drag_f is force divided by mass (m/s^2)
        drag_f = -0.5 * RHO * CD * AREA / M * v_mag

    # Resolution of forces into Cartesian acceleration components
    ax = drag_f * vx_rel
    ay = (drag_f * vy_rel) - G

    return [vx, vy, ax, ay]

def rk4_step(state, dt):
    """
    4th-Order Runge-Kutta integration to handle the ODE system.
    Chosen to maintain O(h^4) global error; Euler would drift too much over 3km.
    """
    k1 = get_rates(state)
    
    s2 = [state[i] + k1[i] * dt / 2 for i in range(4)]
    k2 = get_rates(s2)
    
    s3 = [state[i] + k2[i] * dt / 2 for i in range(4)]
    k3 = get_rates(s3)
    
    s4 = [state[i] + k3[i] * dt for i in range(4)]
    k4 = get_rates(s4)

    new_state = []
    for i in range(4):
        # Weighted slope average across the step
        slope = (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) / 6
        new_state.append(state[i] + slope * dt)

    return new_state

# Elevation profile for the Waterloo/Mont-Saint-Jean ridge line
TERRAIN_POINTS = [
    (0.0, 50.0),    
    (500.0, 50.0),  
    (1000.0, 60.0), 
    (1500.0, 55.0), 
    (3000.0, 55.0)  
]

def get_terrain_height(x):
    """
    Linear interpolation between topographic data points for collision detection.
    """
    if x <= TERRAIN_POINTS[0][0]:
        return TERRAIN_POINTS[0][1]
    
    for i in range(len(TERRAIN_POINTS) - 1):
        xa, ya = TERRAIN_POINTS[i]
        xb, yb = TERRAIN_POINTS[i+1]
        if x < xb: 
            # Linear map between nodes: y = ya + (yb-ya)*(x-xa)/(xb-xa)
            return ya + (yb - ya) * ((x - xa) / (xb - xa))
        
    return TERRAIN_POINTS[-1][1]

# --- MAIN EXECUTION ---
trajectory = [(X0, Y0)]

# Integration loop: Terminates on terrain collision or watchdog timeout
while S[1] >= get_terrain_height(S[0]):
    if T > 60: # Watchdog limit for high-angle failures
        break

    S = rk4_step(S, DT)
    T += DT
    trajectory.append((S[0], S[1]))

# Final data dump to stdout
print("\n" + "="*35)
print("      SIMULATION OUTPUT DATA")
print("-" * 35)
print(f"Launch Angle:   {ANGLE_DEG}°")
print(f"Impact Range:   {S[0]:.2f} m")
print(f"Flight Time:    {T:.2f} s")
print(f"Impact Y:       {S[1]:.2f} m")
print(f"Muzzle Vel:     {V0} m/s")
print("="*35 + "\n")

# Optional Plotting Block
try:
    import matplotlib.pyplot as plt

    # Unzipping coordinates for Matplotlib
    x_traj, y_traj = zip(*trajectory)
    x_env = list(range(int(TERRAIN_POINTS[-1][0]) + 1))
    y_env = [get_terrain_height(x) for x in x_env]
    
    plt.figure(figsize=(10, 5))
    plt.plot(x_env, y_env, 'g', label='Waterloo Ridge Elevation', linewidth=2)
    plt.fill_between(x_env, y_env, color='g', alpha=0.1)
    plt.plot(x_traj, y_traj, 'r--', label='Projectile Trajectory')
    
    plt.title(f'9lb Ballistic Simulation ({ANGLE_DEG} deg)')
    plt.xlabel('Distance (m)')
    plt.ylabel('Altitude (m)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

except ImportError:
    print("Matplotlib not found; skipping visual plots.")
