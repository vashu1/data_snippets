? midaco mentioned http://www.pyopt.org/examples/examples.html

Comparison between original Galileo and MIDACO Missions
https://www.researchgate.net/figure/Comparison-between-original-Galileo-and-MIDACO-Missions_tbl1_236622138

? Bonmin

https://www.wikiwand.com/en/Comparison_of_optimization_software

midaco old example http://www.pyopt.org/examples/examples.parallel_midaco.html

# OpenGoddard

pip3 install OpenGoddard



# GEKKO

https://apmonitor.com/wiki/index.php/Apps/RocketLaunch

https://github.com/BYU-PRISM/GEKKO

# RocketPy

pip3 install rocketpy

# scipy.optimize.minimize

# Differential Evolution Optimization

https://medium.com/analytics-vidhya/optimization-modelling-in-python-metaheuristics-with-constraints-c22b08c487e8

https://medium.com/analytics-vidhya/optimization-modelling-in-python-multiple-objectives-760b9f1f26ee
Often Pareto-optimal solutions can be joined by line or surface. Such boundary is called Pareto-optimal front.

https://medium.com/analytics-vidhya/dynamic-optimization-in-python-rocket-soft-landing-a5a68eaf3b94

python optimization module Pyomo with nonlinear solver Ipopt

real landings are simulated using model predictive control techniques. 
At each time step system receives state feedback on its actual and predicted 
position in space, and then auto-corrects itself (using thrusters and actuated 
fins) if deviation is too high.

---

? Hermite–Simpson collocation

https://www.matthewpeterkelly.com/research/MatthewKelly_IntroTrajectoryOptimization_SIAM_Review_2017.pdf

many ways that trajectory optimization can go wrong

One particularly tricky type of bug occurs when there is a family of optimal solutions, rather than a single
unique solution. This causes a failure to converge because the optimization is searching for a locally optimal
solution, which it never finds because many solutions are equally good. The fix is to modify the problem
statement so that there is a unique solution. One simple way to do this is to add a small regularization
term to the cost function, such as the integral of control squared along the trajectory. This puts a shallow
bowl in the objective function, forcing a unique solution. Trajectory optimization problems with non-unique
solutions often have singular arcs, which occur when the optimal control is not uniquely defined by the
objective function. 

A trajectory optimization problem with a non-smooth solution (control) might cause the non-linear
program to converge very slowly. This occurs in our final example: finding the minimal work trajectory to
move a block between two points (§8). There three basic ways to deal with a discontinuous solution (control).
The first is to do mesh refinement (§5.2) so that there are many short segments near the discontinuity. The
second is to slightly modify the problem, typically by introducing a smoothing term, such that the solution
is numerically stiff but not discontinuous. This second approach was used in [55]. The third approach is to
solve the problem using a multi-phase method (see §9.9), such that the control in each phase of the trajectory
is continuous, and discontinuities occur between phases.

Another common cause of poor convergence in the non-linear programming solver occurs when then ob-
jective and constraint functions are not consistent (see §5.5). There are many sources of inconsistency that
find their way into trajectory optimization problems: discontinuous functions (abs(), min(), max()...),
random number generators, variable step (adaptive) integration, iterative root finding, and table interpo-
lation. All of these will cause significant convergence problems if placed inside of a standard non-linear
programming solver. Section §5.5 covers some methods for handling inconsistent functions

---

https://ru.wikipedia.org/wiki/%D0%9E%D0%BF%D1%82%D0%B8%D0%BC%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5_%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5#%D0%9F%D1%80%D0%B8%D0%BD%D1%86%D0%B8%D0%BF_%D0%BC%D0%B0%D0%BA%D1%81%D0%B8%D0%BC%D1%83%D0%BC%D0%B0_%D0%9F%D0%BE%D0%BD%D1%82%D1%80%D1%8F%D0%B3%D0%B8%D0%BD%D0%B0

вариационное исчисление, принцип максимума Понтрягина и динамическое программирование Беллмана

---

https://en.wikipedia.org/wiki/Trajectory_optimization

Collocation method (Simultaneous Method)
    A transcription method that is based on function approximation, typically using implicit Runge--Kutta schemes.

Directly approximates 𝑥(𝑡) and 𝑢 𝑡
•Piecewise: eg. Hermite-Simpson method
•Global: eg. Pseudospectral methods

Pseudospectral method (Global Collocation)
    A transcription method that represents the entire trajectory as a single high-order orthogonal polynomial.
Pseudospectral Methods
•Represent entire state trajectory as sum of weighted basis functions
•Chebyshev polynomials, Legendre polynomials, etc.
https://coursys.sfu.ca/2019fa-cmpt-419-x1/pages/Collocation/view
Cons:
•Dense optimization problems

Mesh refinement - clooser knot if nonlinear ot important area

---

# PyKEP, PyGMO

(Open Source, from the European Space Agency for interplanetary trajectory optimization)
Examples
    Multiple impulses transfer between Earth and Venus
    Multi revolutions Lambert Problem
    Orbital parameters (osculating and modified equinoctial)
    Lunar orbit propagation with degree 20 spherical harmonics gravity model
    Using SPICE kernels to study HERA trajectory
...
Global optimization of a multiple gravity assist trajectory with one deep space manouvre per leg

# MIDACO

MIDACO holds several record solutions on interplanetary spaceflight trajectory design problems[3][4][5][6] made publicly available by European Space Agency

Optimization software particularly developed for interplanetary space trajectories. (Avail. in Matlab, Octave, Python, C/C++, R and Fortran)
...
MIDACO was created in collaboration of European Space Agency and EADS Astrium to solve constrained mixed-integer non-linear (MINLP) space applications.
http://www.midaco-solver.com/
...
MIDACO solves problems with up to 100,000 variable
...
combining an extended evolutionary Ant Colony
Optimization (ACO) [34] algorithm with the Oracle Penalty Method [36] for constrained handling.

Like the majority of evolutionary optimization algorithms, MIDACO considers the objective f(x)
and constraint g(x) functions as black-box functions

This black-box concept gives the user absolute freedom to formulate the problem in any de-
sired way
any kind of programming statement
(like if-clauses or subroutine calls) or even call exeternal programs (like Simulink or Text-I/O

# Gekko

(optimization software): A Python optimization package[51] with trajectory optimization applications of HALE Aircraft[52] and aerial towed cable systems.

# HamPath

On solving optimal control problems by indirect and path following methods (Matlab and Python interfaces).

https://www.hampath.org/description/

~/Downloads/hampath307

# Opty

Python package utilizing SymPy for symbolic description of ordinary differential equations to form constraints needed to solve optimal control and parameter identification problems using the direct collocation method and non-linear programming.

# OpenGoddard

An open source optimal control software package written in Python that uses pseudospectral methods.

# beluga

An open source Python package for trajectory optimization using indirect methods.

# SciPy

https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html