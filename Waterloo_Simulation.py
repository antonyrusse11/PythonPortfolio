import math 

# Simulation Params
T = 0
DT = 0.01
X0, Y0 = 0.0, 50.0 

# 9lb Projectile & Environment
M = 4.08    
D = 0.102 
AREA = math.pi * (D/2)**2 
CD = 0.45 
G = 9.81 
RHO = 1.225 
V0 = 450.0 
WIND_X, WIND_Y = 5.0, -1.0

ANGLE_DEG = 10.0
RADS = math.radians(ANGLE_DEG)

# State: [x, y, vx, vy]
S = [X0, Y0, V0 * math.cos(RADS), V0 * math.sin(RADS)]

def get_rates(state):
    x, y, vx, vy = state

    # Relative velocity for drag
    vx_rel = vx - WIND_X 
    vy_rel = vy - WIND_Y 
    v_mag = math.sqrt(vx_rel**2 + vy_rel**2)

    if v_mag == 0:
        drag_f = 0.0
    else:
        drag_f = -0.5 * RHO * CD * AREA / M * v_mag

    ax = drag_f * vx_rel
    ay = (drag_f * vy_rel) - G

    return [vx, vy, ax, ay]

def rk4_step(state, dt):
    """Standard RK4 integration"""
    k1 = get_rates(state)
    
    s2 = [state[i] + k1[i] * dt / 2 for i in range(4)]
    k2 = get_rates(s2)
    
    s3 = [state[i] + k2[i] * dt / 2 for i in range(4)]
    k3 = get_rates(s3)
    
    s4 = [state[i] + k3[i] * dt for i in range(4)]
    k4 = get_rates(s4)

    new_state = []
    for i in range(4):
        # Weighted average of slopes
        slope = (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) / 6
        new_state.append(state[i] + slope * dt)

    return new_state

# Waterloo Terrain Profile
TERRAIN_POINTS = [
    (0.0, 50.0),    
    (500.0, 50.0),  
    (1000.0, 60.0), 
    (1500.0, 55.0), 
    (3000.0, 55.0)  
]

def get_terrain_height(x):
    if x <= TERRAIN_POINTS[0][0]:
        return TERRAIN_POINTS[0][1]
    
    for i in range(len(TERRAIN_POINTS) - 1):
        xa, ya = TERRAIN_POINTS[i]
        xb, yb = TERRAIN_POINTS[i+1]
        if x < xb: 
            return ya + (yb - ya) * ((x - xa) / (xb - xa))
        
    return TERRAIN_POINTS[-1][1]

# Main Sim Loop
trajectory = [(X0, Y0)]

while S[1] >= get_terrain_height(S[0]):
    if T > 60: # Watchdog
        break

    S = rk4_step(S, DT)
    T += DT
    trajectory.append((S[0], S[1]))

# --- Results Output ---
print("\n" + "="*35)
print("      SIMULATION RESULTS")
print("-" * 35)
print(f"Launch Angle:   {ANGLE_DEG}°")
print(f"Final Range:    {S[0]:.2f} m")
print(f"Flight Time:    {T:.2f} s")
print(f"Impact Height:  {S[1]:.2f} m")
print(f"Muzzle Vel:     {V0} m/s")
print("="*35 + "\n")

# --- Visuals ---
try:
    import matplotlib.pyplot as plt

    x_traj, y_traj = zip(*trajectory)
    x_env = list(range(int(TERRAIN_POINTS[-1][0]) + 1))
    y_env = [get_terrain_height(x) for x in x_env]
    
    plt.figure(figsize=(10, 5))
    plt.plot(x_env, y_env, 'g', label='Waterloo Ridge', linewidth=2)
    plt.fill_between(x_env, y_env, color='g', alpha=0.1)
    plt.plot(x_traj, y_traj, 'r--', label='Shot Trajectory')
    
    plt.title(f'9lb Cannonball Ballistics ({ANGLE_DEG} deg)')
    plt.xlabel('Distance (m)')
    plt.ylabel('Altitude (m)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

except ImportError:
    print("Matplotlib missing. Visuals skipped.")
