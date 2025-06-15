import math
import sympy
RF_goal = 0.9

#First approach to bypass the complexity of column buckling reverse engineering
#I_over_A has to be replaced by a function for the ratio of I_yy over A_tot which inly depends on DIM1, DIM2, DIM3, DIM4 and thickness_skin by plugging back the equations in the code below (pretty work-intensive task)

#Reverse engineering of DIM1 for Euler buckling for DIM2, DIM3, DIM4 and thickness_skin unchanged
def reverseColumn_Euler_DIM1(RF_goal, DIM2, DIM3, DIM4, stringer_pitch, thickness_skin, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = sigma_crit*c**2*length**2/math.pi**2*EModulus
    DIM1 = sympy.symbols('DIM1')
    optimization = sympy.Eq(I_over_A, I_by_A)
    DIM1_rev = sympy.solve(optimization, DIM1)
    return DIM1_rev

#Reverse engineering of DIM2 for Euler for DIM1, DIM3, DIM4 and thickness_skin unchanged
def reverseColumn_Euler_DIM2(RF_goal, DIM1, DIM3, DIM4, stringer_pitch, thickness_skin, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = sigma_crit*c**2*length**2/math.pi**2*EModulus
    DIM2 = sympy.symbols('DIM2')
    optimization = sympy.Eq(I_over_A, I_by_A)
    DIM2_rev = sympy.solve(optimization, DIM2)
    return DIM2_rev

#Reverse engineering of DIM3 for Euler for DIM1, DIM2, DIM4 and thickness_skin unchanged
def reverseColumn_Euler_DIM3(RF_goal, DIM1, DIM2, DIM4, stringer_pitch, thickness_skin, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = sigma_crit*c**2*length**2/math.pi**2*EModulus
    DIM3 = sympy.symbols('DIM3')
    optimization = sympy.Eq(I_over_A, I_by_A)
    DIM3_rev = sympy.solve(optimization, DIM3)
    return DIM3_rev

#Reverse engineering of DIM4 for Euler for DIM1, DIM2, DIM3 and thickness_skin unchanged
def reverseColumn_Euler_DIM4(RF_goal, DIM1, DIM2, DIM3, stringer_pitch, thickness_skin, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = sigma_crit*c**2*length**2/math.pi**2*EModulus
    DIM4 = sympy.symbols('DIM4')
    optimization = sympy.Eq(I_over_A, I_by_A)
    DIM4_rev = sympy.solve(optimization, DIM4)
    return DIM4_rev

#Reverse engineering of thickness_skin for Euler for DIM1, DIM2, DIM2 and DIM4 unchanged
def reverseColumn_Euler_thickness_skin(RF_goal, DIM1, DIM2, DIM3, DIM4, stringer_pitch, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = sigma_crit*c**2*length**2/math.pi**2*EModulus
    thickness_skin = sympy.symbols('thickness_skin')
    optimization = sympy.Eq(I_over_A, I_by_A)
    thickness_skin_rev = sympy.solve(optimization, thickness_skin)
    return thickness_skin_rev
#Has to be decided if thickness_skin should be rverse engineered for column buckling, biaxial panel buckling and shear panel buckling and then the maximum is used for optimization
