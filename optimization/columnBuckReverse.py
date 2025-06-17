import math
import sympy
RF_goal = 0.9

#First approach to bypass the complexity of column buckling reverse engineering

#Reverse engineering of DIM1 for Euler buckling for DIM2, DIM3, DIM4 and thickness_skin unchanged
def reverseColumn_Euler_DIM1(RF_goal, DIM02, DIM03, DIM04, stringer_pitch_in, thickness_skin_in, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = abs(sigma_crit)*(c**2*length**2)/(math.pi**2*EModulus)
    DIM1 = sympy.symbols('DIM1')
    DIM2 = DIM02
    DIM3 = DIM03
    DIM4 = DIM04
    stringer_pitch = stringer_pitch_in
    thickness_skin = thickness_skin_in
    I_over_A = ((stringer_pitch*thickness_skin**3)/12+(stringer_pitch*thickness_skin*(-thickness_skin/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2)+(DIM3*DIM2**3)/12+(DIM3*DIM2*(DIM1-DIM2/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2)+2*(DIM2*(DIM1-DIM2)**3)/12+2*(DIM2*(DIM1-DIM2)*((DIM1-DIM2)/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2)+2*(DIM4*DIM2**3)/12+2*(DIM4*DIM2*(DIM2/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2))/(stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)
    opt_eq = sympy.simplify(I_over_A)
    optimization = sympy.Eq(opt_eq, I_by_A)
    DIM1_rev = sympy.nsolve(optimization, DIM1, 25)
    return DIM1_rev

#Reverse engineering of DIM2 for Euler for DIM1, DIM3, DIM4 and thickness_skin unchanged
def reverseColumn_Euler_DIM2(RF_goal, DIM01, DIM03, DIM04, stringer_pitch_in, thickness_skin_in, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = abs(sigma_crit)*(c**2*length**2)/(math.pi**2*EModulus)
    DIM1 = DIM01
    DIM2 = sympy.symbols('DIM2')
    DIM3 = DIM03
    DIM4 = DIM04
    stringer_pitch = stringer_pitch_in
    thickness_skin = thickness_skin_in
    I_over_A = ((stringer_pitch*thickness_skin**3)/12+stringer_pitch*thickness_skin*(-thickness_skin/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2+(DIM3*DIM2**3)/12+DIM3*DIM2*(DIM1-DIM2/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2+2*(DIM2*(DIM1-DIM2)**3)/12+2*DIM2*(DIM1-DIM2)*((DIM1-DIM2)/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2+2*(DIM4*DIM2**3)/12+2*DIM4*DIM2*(DIM2/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2
    optimization = sympy.Eq(I_over_A, I_by_A)
    DIM2_rev = sympy.solve(optimization, DIM2)
    return DIM2_rev

#Reverse engineering of DIM3 for Euler for DIM1, DIM2, DIM4 and thickness_skin unchanged
def reverseColumn_Euler_DIM3(RF_goal, DIM01, DIM02, DIM04, stringer_pitch_in, thickness_skin_in, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = abs(sigma_crit)*(c**2*length**2)/(math.pi**2*EModulus)
    DIM1 = DIM01
    DIM2 = DIM02
    DIM3 = sympy.symbols('DIM3')
    DIM4 = DIM04
    stringer_pitch = stringer_pitch_in
    thickness_skin = thickness_skin_in
    I_over_A = ((stringer_pitch*thickness_skin**3)/12+stringer_pitch*thickness_skin*(-thickness_skin/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2+(DIM3*DIM2**3)/12+DIM3*DIM2*(DIM1-DIM2/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2+2*(DIM2*(DIM1-DIM2)**3)/12+2*DIM2*(DIM1-DIM2)*((DIM1-DIM2)/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2+2*(DIM4*DIM2**3)/12+2*DIM4*DIM2*(DIM2/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2
    optimization = sympy.Eq(I_over_A, I_by_A)
    DIM3_rev = sympy.solve(optimization, DIM3)
    return DIM3_rev

#Reverse engineering of DIM4 for Euler for DIM1, DIM2, DIM3 and thickness_skin unchanged
def reverseColumn_Euler_DIM4(RF_goal, DIM01, DIM02, DIM03, stringer_pitch_in, thickness_skin_in, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = abs(sigma_crit)*(c**2*length**2)/(math.pi**2*EModulus)
    DIM1 = DIM01
    DIM2 = DIM02
    DIM3 = DIM03
    DIM4 = sympy.symbols('DIM4')
    stringer_pitch = stringer_pitch_in
    thickness_skin = thickness_skin_in
    I_over_A = ((stringer_pitch*thickness_skin**3)/12+stringer_pitch*thickness_skin*(-thickness_skin/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2+(DIM3*DIM2**3)/12+DIM3*DIM2*(DIM1-DIM2/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2+2*(DIM2*(DIM1-DIM2)**3)/12+2*DIM2*(DIM1-DIM2)*((DIM1-DIM2)/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2+2*(DIM4*DIM2**3)/12+2*DIM4*DIM2*(DIM2/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2
    optimization = sympy.Eq(I_over_A, I_by_A)
    DIM4_rev = sympy.solve(optimization, DIM4)
    return DIM4_rev

#Reverse engineering of thickness_skin for Euler for DIM1, DIM2, DIM2 and DIM4 unchanged
def reverseColumn_Euler_thickness_skin(RF_goal, DIM01, DIM02, DIM03, DIM04, stringer_pitch_in, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = abs(sigma_crit)*(c**2*length**2)/(math.pi**2*EModulus)
    DIM1 = DIM01
    DIM2 = DIM02
    DIM3 = DIM03
    DIM4 = DIM04
    stringer_pitch = stringer_pitch_in
    thickness_skin = sympy.symbols('thickness_skin')
    I_over_A = ((stringer_pitch*thickness_skin**3)/12+stringer_pitch*thickness_skin*(-thickness_skin/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2+(DIM3*DIM2**3)/12+DIM3*DIM2*(DIM1-DIM2/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2+2*(DIM2*(DIM1-DIM2)**3)/12+2*DIM2*(DIM1-DIM2)*((DIM1-DIM2)/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2+2*(DIM4*DIM2**3)/12+2*DIM4*DIM2*(DIM2/2-(stringer_pitch*thickness_skin*(-thickness_skin/2)+DIM3*DIM2*(DIM1-DIM2/2)+2*DIM2*(DIM1-DIM2)*(DIM1-DIM2)/2+2*DIM4*DIM2*DIM2/2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2)**2)/stringer_pitch*thickness_skin+DIM3*DIM2+2*DIM2*DIM1-2*DIM2**2+2*DIM4*DIM2
    optimization = sympy.Eq(I_over_A, I_by_A)
    thickness_skin_rev = sympy.solve(optimization, thickness_skin)
    return thickness_skin_rev
#Has to be decided if thickness_skin should be rverse engineered for column buckling, biaxial panel buckling and shear panel buckling and then the maximum is used for optimization

#testcase for column buckling reverse engineering
if __name__ == '__main__':
    testopt_DIM1 = reverseColumn_Euler_DIM1(RF_goal=0.9, DIM02=2, DIM03=20, DIM04=15, stringer_pitch_in=200, thickness_skin_in=4, length=750, c=1, EModulus=65241.07, sigma_applied=-80.922204)
    print(testopt_DIM1)