# ---- PHYSICAL CONSTANTS
c = 299792458 # m s-1, speed of light
b = 2.897771955e-3 # m K, Wien's displacement constant
h = 6.62607015e-34 # J Hz-1, Planck constant
PI = 3.1415926535897932384626433 # regular everyday pi
sigma = 5.670374419e-8 # W m-2 K-4, Stefan-Boltzmann constant

# ---- DESIGN INPUTS
# -- reactor
dry_mass = 50000 # kg
conversion_ratio = 0.1 # 10% of fission mass converted into energy
e_reactor = 0.7 # reactor efficiency
fissile_mass = 20000 # kg
P_reactor = 100e6 # W, nuclear reactor power

# -- thruster
A_radiator = 10 # m2, radiator area
emissivity = 0.5

# ---- FORMULAE
def get_radiant_emmittance(T, epsilon=1):
    global sigma
    return epsilon * sigma * T**4 # J m-2 s-1

def get_radiance(T, A, epsilon=1):
    return get_radiant_emmittance(T, epsilon) * A # W

def get_T(P, A, epsilon=1):
    global sigma
    return (P/(epsilon * sigma * A)) ** (0.25)

def get_reactor_mass(P_reactor):
    return P_reactor / 1.5e3 # kg, assuming 1.5 kW per kg, somewhat conservative

def get_total_energy_output(m):
    global c
    return m * c**2 # J

def get_ideal_delta_v(m_dry, m_fuel):
    global c
    m_i = m_dry + m_fuel
    m_f = m_dry
    numerator = c * ((m_i/m_f)**2 - 1)
    denominator = (m_i/m_f)**2 + 1
    return numerator / denominator

# ---- CALCULATIONS
print("Calculating...")
total_available_energy = get_total_energy_output(fissile_mass * conversion_ratio * e_reactor)
run_time = total_available_energy / P_reactor # s
mdot = fissile_mass / run_time # kg s-1
m_reactor = get_reactor_mass(P_reactor)
dry_mass += m_reactor
P_propulsion = P_reactor * e_reactor
thrust = 2 * P_propulsion / c # N
T_thruster = get_T(P_propulsion, A_radiator, emissivity)
delta_v = get_ideal_delta_v(dry_mass + fissile_mass * (1 - conversion_ratio), fissile_mass * conversion_ratio)
delta_v_ideal = get_ideal_delta_v(dry_mass, fissile_mass)
avg_accel = delta_v / run_time

# ---- OUTPUT
print("Total available energy:", total_available_energy, "J =", total_available_energy/1e6, "MJ")
print("Total emission time:", run_time, "s =", run_time / (60 * 60 * 24 * 365), "years")
print("Fissile fuel consumption rate:", mdot, "kg/s =", mdot * 1e6 * 60 * 60, "mg/hour")
print("Reactor mass:", m_reactor, "kg =", m_reactor/1e3, "t")
print("Propulsion power:", P_propulsion, "W =", P_propulsion/1e6, "MW")
print("Thrust:", thrust, "N")
print("Thruster temperature:", T_thruster, "K =", T_thruster-273, "degrees C")
print("Delta-v:", delta_v, "m/s =", delta_v/1e3, "km/s =", delta_v / c, "c")
print("Ideal delta-v", delta_v_ideal, "m/s =", delta_v_ideal/1e3, "km/s =", delta_v_ideal / c, "c")
print("Average acceleration:", avg_accel, "m/s per second =", avg_accel * 60 * 60 * 24 * 365/1e3, "km/s per year")
