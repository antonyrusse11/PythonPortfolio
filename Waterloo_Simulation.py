#Importing Essential Libraries
import math 

# --- 0. Initialise State Variables ---
t = 0
x0 = 0.0 # Starting horizontal position (meters)
y0 = 0.0 # Starting vertical position (meters) - Assumed ground level
time_step = 0.01

# --- Define Initial Position ---
x0 = 0.0 # Starting horizontal position (meters)
y0 = 50.0  # Starting vertical position (meters) - Must match launch altitude in TERRAIN_POINTS

# --- 1. Physical Constants ---
# --- 9 Pounder Projectile Parameters ---- 

M = 4.08    # mass (kg) - approx 9 pounder  
D = 0.102 # diameter (m)
A = math.pi * (D/2)**2 # cross-sectional area (m^2)
Cd = 0.45 # drag coefficient 

# --- Environmental Parameters ---

G = 9.81 # gravity (m/s^2)
RHO = 1.225 # air density (kg/m^3)
V0 = 450.0 # muzzle velocity (m/s)
WIND_X = 5.0 # horizontal wind speed (m/s)
WIND_Y = -1.0 # vertical wind speed (m/s). Negative indicates a downdraft.

#Launch Angle Input
ANGLE_DEG = 10.0 # Launch Angle (degrees)

# --- 2. Initial Velocity Calculation ---

# Convert angle to radians
ANGLE_RAD = math.radians(ANGLE_DEG)

# Calculate initial velocity components
vx0 = V0 * math.cos(ANGLE_RAD)
vy0 = V0 * math.sin(ANGLE_RAD)

# Initial State Vector: S = [x, y, vx, vy]
S = [x0, y0, vx0, vy0]

# --- 3. Rate of Change Function (Physics Model) ---

def calculate_rates(state):
    """
    Calculates the time derivatives (vx, vy, ax, ay) given the current state.
    state = [x, y, vx, vy]
    """
    x, y, vx, vy = state

    # 1. Calculate Relative Velocity (V_rel = V_ball - V_wind)
    # Both horizontal and vertical wind components are now subtracted.
    vx_rel = vx - WIND_X 
    vy_rel = vy - WIND_Y 
    V_rel_mag = math.sqrt(vx_rel**2 + vy_rel**2)

    # 2. Calculate Drag Force and Acceleration (a = F_drag / M)

    if V_rel_mag == 0:
        drag_factor = 0.0
    else:
        drag_factor = -0.5 * RHO * Cd * A / M * V_rel_mag

    # Drag acceleration components
    ax_drag = drag_factor * vx_rel
    ay_drag = drag_factor * vy_rel

    # 3. Calculate Net Acceleration
    ax = ax_drag
    ay = ay_drag - G

    # The rates of change (dS/dt)
    return [vx, vy, ax, ay]

# --- 5. Runge-Kutta 4 (RK4) Step ---

def rk4_step(S, t, dt):
    """Performs one RK4 step to advance the state S by time dt."""

    # K1: Rate at start of interval
    k1_rates = calculate_rates(S)
    k1 = [dt * rate for rate in k1_rates]

    # K2: Rate at midpoint 1 (uses k1 to estimate S_mid)
    # S_mid_1 = S + k1/2
    S_mid_1 = [S[i] + k1[i]/2 for i in range(4)]
    k2_rates = calculate_rates(S_mid_1)
    k2 = [dt * rate for rate in k2_rates]

    # K3: Rate at midpoint 2 (uses k2 to estimate S_mid)
    # S_mid_2 = S + k2/2
    S_mid_2 = [S[i] + k2[i]/2 for i in range(4)]
    k3_rates = calculate_rates(S_mid_2)
    k3 = [dt * rate for rate in k3_rates]

    # K4: Rate at end of interval (uses k3 to estimate S_end)
    # S_end = S + k3
    S_end = [S[i] + k3[i] for i in range(4)]
    k4_rates = calculate_rates(S_end)
    k4 = [dt * rate for rate in k4_rates]

    # Calculate New State (S_new) using the weighted average:
    # S_new = S + (1/6) * (k1 + 2*k2 + 2*k3 + k4)
    S_new = []
    for i in range(4):
        # Calculate the change (delta) for each of the four state variables
        delta = (1/6) * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i])
        S_new.append(S[i] + delta)

    return S_new

# --- 6. Terrain Model (Geometry) ---

# Define the terrain profile for Waterloo as a list of (x, y) coordinates (meters)

TERRAIN_POINTS = [
    (0.0, 50.0),        # Cannon launch point altitude
    (500.0, 50.0),      # Flat for 500m
    (1000.0, 60.0),     # Ridge peak (e.g., Mont Saint-Jean)
    (1500.0, 55.0),     # Gentle downslope
    (3000.0, 55.0)      # Final ground altitude
]

def terrain(x):
    """Calculates terrain height at horizontal position x using linear interpolation."""

    # 1. Edge Case: Before the start
    if x <= TERRAIN_POINTS[0][0]:
        return TERRAIN_POINTS[0][1]
    
    # 2. Find the correct segment
    for i in range(len(TERRAIN_POINTS) - 1):
        xa, ya = TERRAIN_POINTS[i]
        xb, yb = TERRAIN_POINTS[i+1]

        if x < xb: 
            #Linear interpolation method formula 
            y_terrain = ya + (yb - ya) * ((x - xa) / (xb - xa))
            return y_terrain
        
    # 3. Edge Case: Beyond the last point
    return TERRAIN_POINTS[-1][1]

# --- 7. Simulation Loop and Output ---

# List to store trajectory points for plotting
trajectory = [(x0, y0)]

# Run the simulation until the cannonball's height (S[1]) is less than or equal to the terrain height
# S[0] is x, S[1] is y
while S[1] >= terrain(S[0]):

    # Safety Check: Limit flight time to prevent infinite loops (e.g., if the cannon shoots straight up)
    if t > 60: #Max 60s flight time
        print("\nSimulation aborted: Flight time exceeded 60 seconds.")
        break

    # Advance the state using RK4
    S = rk4_step(S, t, time_step)
    t += time_step

    # Store the new position
    trajectory.append((S[0], S[1]))

# --- 8. Final Results and Visualization ---

final_range = S[0]
print(f"\n--- Simulation Results ---")
print(f"Launch Angle: {ANGLE_DEG} degrees")
print(f"Final Horizontal Range: {final_range:.2f} meters")
print(f"Final Flight Time: {t:.2f} seconds")
print(f"Note: Drag and Wind Factors included in calculations.")
print("\n")

# --- Matplotlib Plotting ---
try:
    import matplotlib.pyplot as plt

    # 1. Prepare Trajectory Data
    x_traj = [p[0] for p in trajectory]
    y_traj = [p[1] for p in trajectory]

    # 2. Prepare Terrain Data (for plotting smooth terrain)
    # Create a dense array of x-points from 0 to 3000m
    x_terrain = [i for i in range(int(TERRAIN_POINTS[-1][0]) + 1)]
    y_terrain = [terrain(x) for x in x_terrain]
    
    # 3. Create the Plot
    plt.figure(figsize=(12, 6))
    
    # Plot the Terrain
    plt.plot(x_terrain, y_terrain, 'g-', label='Waterloo Terrain Profile', linewidth=2)
    plt.fill_between(x_terrain, y_terrain, min(y_terrain) - 10, color='lightgreen', alpha=0.5)

    # Plot the Trajectory
    plt.plot(x_traj, y_traj, 'r--', label='Cannonball Trajectory (RK4)')
    
    # Mark the impact point
    plt.plot(final_range, terrain(final_range), 'ro', markersize=8, label='Impact Point')

    plt.title(f'9-Pounder Cannon Range Simulation (Angle: {ANGLE_DEG}°)')
    plt.xlabel('Horizontal Distance (m)')
    plt.ylabel('Altitude (m)')
    plt.grid(True)
    plt.legend()
    plt.axis('equal') # Optional: Makes the scale representative
    plt.ylim(min(y_terrain) - 10, max(y_traj) * 1.1) # Set Y limits dynamically
    plt.show()

except ImportError:
    print("\nWarning: Matplotlib not found. Install it to visualize the results.")
