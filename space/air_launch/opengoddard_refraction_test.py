from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from OpenGoddard.optimize import Problem, Guess, Condition, Dynamics

START = (0,0)
END = (1,1)
FST_THICKNESS = 0.5
assert FST_THICKNESS < END[1]
FST_SPEED = 1
SND_SPEED = 10

START_DEGREE = 45

class Ball:
    def __init__(self):
        self.theta0 = np.deg2rad(START_DEGREE)  # limit and initial angle


def dynamics(prob, obj, section):
    #x = prob.states(0, section)
    y = prob.states(1, section)
    theta = prob.controls(0, section)

    #print(type(y))
    #v = FST_SPEED if y < FST_THICKNESS else SND_SPEED
    #v = np.where(y < FST_THICKNESS, FST_SPEED, SND_SPEED)
    v = 1+y*10  # need smooth change

    dx = Dynamics(prob, section)
    dx[0] = v * np.sin(theta)
    dx[1] = v * np.cos(theta)
    return dx()


def equality(prob, obj):
    x = prob.states_all_section(0)
    y = prob.states_all_section(1)
    # theta = prob.controls_all_section(0)
    # tf = prob.time_final(-1)

    result = Condition()

    # event condition
    result.equal(x[0], START[0])
    result.equal(y[0], START[1])
    result.equal(x[-1], END[0])
    result.equal(y[-1], END[1])

    return result()


def inequality(prob, obj):
    x = prob.states_all_section(0)
    y = prob.states_all_section(1)
    theta = prob.controls_all_section(0)
    tf = prob.time_final(-1)

    result = Condition()

    # lower bounds
    #result.lower_bound(tf, 0.1)
    #result.lower_bound(y, START[1])
    #result.lower_bound(theta, 0)

    # upper bounds
    # result.upper_bound(theta, np.pi/2)
    # result.upper_bound(y, x * np.tan(obj.theta0) + obj.h)

    return result()


def cost(prob, obj):
    tf = prob.time_final(-1)
    return tf


def cost_derivative(prob, obj):
    jac = Condition(prob.number_of_variables)
    # index_tf = prob.index_time_final(0)
    index_tf = prob.index_time_final(-1)
    jac.change_value(index_tf, 1)
    return jac()

# ========================
plt.close("all")
plt.ion()
# Program Starting Point
time_init = [0.0, 10.0]
n = [11]
num_states = [2]
num_controls = [1]
max_iteration = 30

flag_savefig = True

savefig_dir = "refraction/normal_"

# ------------------------
# set OpenGoddard class for algorithm determination
prob = Problem(time_init, n, num_states, num_controls, max_iteration)
obj = Ball()

# ========================
# Initial parameter guess
theta_init = Guess.linear(prob.time_all_section, np.deg2rad(START_DEGREE), np.deg2rad(START_DEGREE))
# Guess.plot(prob.time_all_section, theta_init, "gamma", "time", "gamma")
# if(flag_savefig):plt.savefig(savefig_dir + "guess_gamma" + savefig_add + ".png")

x_init = Guess.linear(prob.time_all_section, 0.0, END[0])
# Guess.plot(prob.time_all_section, x_init, "x", "time", "x")
# if(flag_savefig):plt.savefig(savefig_dir + "guess_x" + savefig_add + ".png")

y_init = Guess.linear(prob.time_all_section, 0.0, END[1])
# Guess.plot(prob.time_all_section, theta_init, "y", "time", "y")
# if(flag_savefig):plt.savefig(savefig_dir + "guess_y" + savefig_add + ".png")

prob.set_states_all_section(0, x_init)
prob.set_states_all_section(1, y_init)
prob.set_controls_all_section(0, theta_init)

# ========================
# Main Process
# Assign problem to SQP solver
prob.dynamics = [dynamics]
prob.knot_states_smooth = []
prob.cost = cost
prob.cost_derivative = cost_derivative
prob.equality = equality
prob.inequality = inequality

prob.solve(obj)

# ========================
# Post Process
# ------------------------
# Convert parameter vector to variable
x = prob.states_all_section(0)
y = prob.states_all_section(1)
gamma = prob.controls_all_section(0)
time = prob.time_update()

# ------------------------
# Visualizetion
plt.figure()
plt.subplot(3, 1, 1)
plt.plot(time, x, marker="o", label="x")
plt.plot(time, y, marker="o", label="y")
for line in prob.time_knots():
    plt.axvline(line, color="k", alpha=0.5)
plt.grid()
plt.ylabel("velocity [m/s]")
plt.legend(loc="best")

plt.subplot(3, 1, 2)
plt.plot(time, gamma, marker="o", label="gamma")
for line in prob.time_knots():
    plt.axvline(line, color="k", alpha=0.5)
plt.grid()
plt.xlabel("time [s]")
plt.ylabel("angle [rad]")
plt.legend(loc="best")

plt.subplot(3, 1, 3)
plt.scatter(x, y)
plt.grid()
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc="best")

if(flag_savefig): plt.savefig(savefig_dir + "plot" + ".png")

plt.show()
