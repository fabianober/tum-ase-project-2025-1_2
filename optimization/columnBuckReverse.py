import math
import sympy

#Reverse engineering of DIM1 for Euler buckling for DIM2, DIM3, DIM4 and thickness_skin unchanged
#Test case for stringer loadcase with RF=0.4 (one iteration/all results are counterchecked and valid)
#DIM1: 25 -> 29.9597
#DIM2: 2 -> 19.988
#DIM3: 20 -> 42.5966
#DIM4: checked once for testing, but results would blow up way too much
#thickness_skin(two solutions depending on solver setting): 4 -> 22.9725 (current setting)/1.6 (actually possible, but would make panel buckling worse) 

def reverseColumn_Euler_DIM1(RF_goal, DIM01, DIM02, DIM03, DIM04, stringer_pitch_in, thickness_skin_in, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = abs(sigma_crit)*(c**2*length**2)/(math.pi**2*EModulus)
    DIM1 = sympy.symbols('DIM1')
    DIM2 = DIM02
    DIM3 = DIM03
    DIM4 = DIM04
    stringer_pitch = stringer_pitch_in
    thickness_skin = thickness_skin_in
    I_y_skin = (stringer_pitch * thickness_skin**3) / 12
    I_y_top = (DIM3 * DIM2**3) / 12
    I_y_webs = 2 * (DIM2 * (DIM1 - DIM2)**3) / 12
    I_y_bottoms = 2 * (DIM4 * DIM2**3) / 12
    A_skin = stringer_pitch * thickness_skin
    A_top = DIM3 * DIM2
    A_bottom = DIM4 * DIM2
    A_side_web = DIM2 * (DIM1 - DIM2)
    A_tot = A_skin + A_top + 2*A_bottom + 2*A_side_web
    z_skin = -thickness_skin / 2
    z_bottom = DIM2 / 2
    z_web = (DIM1 - DIM2) / 2
    z_top = DIM1 - DIM2 / 2
    z_bar = (
        A_skin * z_skin +
        A_top * z_top +
        2 * A_side_web * z_web +
        2 * A_bottom * z_bottom
    ) / A_tot
    I_over_A = (I_y_skin + A_skin * (z_skin - z_bar)**2 + I_y_top + A_top * (z_top - z_bar)**2 + I_y_webs + 2 * A_side_web * (z_web - z_bar)**2 + I_y_bottoms + 2 * A_bottom * (z_bottom - z_bar)**2)/A_tot
    optimization = sympy.Eq(I_over_A, I_by_A)
    DIM1_rev = sympy.nsolve(optimization, DIM1, DIM01)
    return DIM1_rev

#Reverse engineering of DIM2 for Euler for DIM1, DIM3, DIM4 and thickness_skin unchanged
def reverseColumn_Euler_DIM2(RF_goal, DIM01, DIM02, DIM03, DIM04, stringer_pitch_in, thickness_skin_in, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = abs(sigma_crit)*(c**2*length**2)/(math.pi**2*EModulus)
    DIM1 = DIM01
    DIM2 = sympy.symbols('DIM2')
    DIM3 = DIM03
    DIM4 = DIM04
    stringer_pitch = stringer_pitch_in
    thickness_skin = thickness_skin_in
    I_y_skin = (stringer_pitch * thickness_skin**3) / 12
    I_y_top = (DIM3 * DIM2**3) / 12
    I_y_webs = 2 * (DIM2 * (DIM1 - DIM2)**3) / 12
    I_y_bottoms = 2 * (DIM4 * DIM2**3) / 12
    A_skin = stringer_pitch * thickness_skin
    A_top = DIM3 * DIM2
    A_bottom = DIM4 * DIM2
    A_side_web = DIM2 * (DIM1 - DIM2)
    A_tot = A_skin + A_top + 2*A_bottom + 2*A_side_web
    z_skin = -thickness_skin / 2
    z_bottom = DIM2 / 2
    z_web = (DIM1 - DIM2) / 2
    z_top = DIM1 - DIM2 / 2
    z_bar = (
        A_skin * z_skin +
        A_top * z_top +
        2 * A_side_web * z_web +
        2 * A_bottom * z_bottom
    ) / A_tot
    I_over_A = (I_y_skin + A_skin * (z_skin - z_bar)**2 + I_y_top + A_top * (z_top - z_bar)**2 + I_y_webs + 2 * A_side_web * (z_web - z_bar)**2 + I_y_bottoms + 2 * A_bottom * (z_bottom - z_bar)**2)/A_tot
    optimization = sympy.Eq(I_over_A, I_by_A)
    DIM2_rev = sympy.nsolve(optimization, DIM2, DIM02)
    return DIM2_rev

#Reverse engineering of DIM3 for Euler for DIM1, DIM2, DIM4 and thickness_skin unchanged
def reverseColumn_Euler_DIM3(RF_goal, DIM01, DIM02, DIM03, DIM04, stringer_pitch_in, thickness_skin_in, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = abs(sigma_crit)*(c**2*length**2)/(math.pi**2*EModulus)
    DIM1 = DIM01
    DIM2 = DIM02
    DIM3 = sympy.symbols('DIM3')
    DIM4 = DIM04
    stringer_pitch = stringer_pitch_in
    thickness_skin = thickness_skin_in
    I_y_skin = (stringer_pitch * thickness_skin**3) / 12
    I_y_top = (DIM3 * DIM2**3) / 12
    I_y_webs = 2 * (DIM2 * (DIM1 - DIM2)**3) / 12
    I_y_bottoms = 2 * (DIM4 * DIM2**3) / 12
    A_skin = stringer_pitch * thickness_skin
    A_top = DIM3 * DIM2
    A_bottom = DIM4 * DIM2
    A_side_web = DIM2 * (DIM1 - DIM2)
    A_tot = A_skin + A_top + 2*A_bottom + 2*A_side_web
    z_skin = -thickness_skin / 2
    z_bottom = DIM2 / 2
    z_web = (DIM1 - DIM2) / 2
    z_top = DIM1 - DIM2 / 2
    z_bar = (
        A_skin * z_skin +
        A_top * z_top +
        2 * A_side_web * z_web +
        2 * A_bottom * z_bottom
    ) / A_tot
    I_over_A = (I_y_skin + A_skin * (z_skin - z_bar)**2 + I_y_top + A_top * (z_top - z_bar)**2 + I_y_webs + 2 * A_side_web * (z_web - z_bar)**2 + I_y_bottoms + 2 * A_bottom * (z_bottom - z_bar)**2)/A_tot
    optimization = sympy.Eq(I_over_A, I_by_A)
    DIM3_rev = sympy.nsolve(optimization, DIM3, DIM03)
    return DIM3_rev

#Reverse engineering of DIM4 for Euler for DIM1, DIM2, DIM3 and thickness_skin unchanged
def reverseColumn_Euler_DIM4(RF_goal, DIM01, DIM02, DIM03, DIM04, stringer_pitch_in, thickness_skin_in, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = abs(sigma_crit)*(c**2*length**2)/(math.pi**2*EModulus)
    DIM1 = DIM01
    DIM2 = DIM02
    DIM3 = DIM03
    DIM4 = sympy.symbols('DIM4')
    stringer_pitch = stringer_pitch_in
    thickness_skin = thickness_skin_in
    I_y_skin = (stringer_pitch * thickness_skin**3) / 12
    I_y_top = (DIM3 * DIM2**3) / 12
    I_y_webs = 2 * (DIM2 * (DIM1 - DIM2)**3) / 12
    I_y_bottoms = 2 * (DIM4 * DIM2**3) / 12
    A_skin = stringer_pitch * thickness_skin
    A_top = DIM3 * DIM2
    A_bottom = DIM4 * DIM2
    A_side_web = DIM2 * (DIM1 - DIM2)
    A_tot = A_skin + A_top + 2*A_bottom + 2*A_side_web
    z_skin = -thickness_skin / 2
    z_bottom = DIM2 / 2
    z_web = (DIM1 - DIM2) / 2
    z_top = DIM1 - DIM2 / 2
    z_bar = (
        A_skin * z_skin +
        A_top * z_top +
        2 * A_side_web * z_web +
        2 * A_bottom * z_bottom
    ) / A_tot
    I_over_A = (I_y_skin + A_skin * (z_skin - z_bar)**2 + I_y_top + A_top * (z_top - z_bar)**2 + I_y_webs + 2 * A_side_web * (z_web - z_bar)**2 + I_y_bottoms + 2 * A_bottom * (z_bottom - z_bar)**2)/A_tot
    optimization = sympy.Eq(I_over_A, I_by_A)
    DIM4_rev = sympy.nsolve(optimization, DIM4, DIM04)
    return DIM4_rev

#Reverse engineering of thickness_skin for Euler for DIM1, DIM2, DIM2 and DIM4 unchanged
def reverseColumn_Euler_thickness_skin(RF_goal, DIM01, DIM02, DIM03, DIM04, stringer_pitch_in, thickness_skin_in, length, c, EModulus, sigma_applied):
    sigma_crit = RF_goal*sigma_applied
    I_by_A = abs(sigma_crit)*(c**2*length**2)/(math.pi**2*EModulus)
    DIM1 = DIM01
    DIM2 = DIM02
    DIM3 = DIM03
    DIM4 = DIM04
    stringer_pitch = stringer_pitch_in
    thickness_skin = sympy.symbols('thickness_skin')
    I_y_skin = (stringer_pitch * thickness_skin**3) / 12
    I_y_top = (DIM3 * DIM2**3) / 12
    I_y_webs = 2 * (DIM2 * (DIM1 - DIM2)**3) / 12
    I_y_bottoms = 2 * (DIM4 * DIM2**3) / 12
    A_skin = stringer_pitch * thickness_skin
    A_top = DIM3 * DIM2
    A_bottom = DIM4 * DIM2
    A_side_web = DIM2 * (DIM1 - DIM2)
    A_tot = A_skin + A_top + 2*A_bottom + 2*A_side_web
    z_skin = -thickness_skin / 2
    z_bottom = DIM2 / 2
    z_web = (DIM1 - DIM2) / 2
    z_top = DIM1 - DIM2 / 2
    z_bar = (
        A_skin * z_skin +
        A_top * z_top +
        2 * A_side_web * z_web +
        2 * A_bottom * z_bottom
    ) / A_tot
    I_over_A = (I_y_skin + A_skin * (z_skin - z_bar)**2 + I_y_top + A_top * (z_top - z_bar)**2 + I_y_webs + 2 * A_side_web * (z_web - z_bar)**2 + I_y_bottoms + 2 * A_bottom * (z_bottom - z_bar)**2)/A_tot
    optimization = sympy.Eq(I_over_A, I_by_A)
    thickness_skin_rev = sympy.nsolve(optimization, thickness_skin, (0, 7*thickness_skin_in), solver='bisect')
    return thickness_skin_rev
#Has to be decided if thickness_skin should be rverse engineered for column buckling, biaxial panel buckling and shear panel buckling and then the maximum is used for optimization

#testcase for column buckling reverse engineering
if __name__ == '__main__':
    testopt_DIM1 = reverseColumn_Euler_DIM1(RF_goal=0.9, DIM01=25, DIM02=2, DIM03=20, DIM04=15, stringer_pitch_in=200, thickness_skin_in=4, length=750, c=1, EModulus=65669.47, sigma_applied=-83.09)
    print(testopt_DIM1)
    testopt_DIM2 = reverseColumn_Euler_DIM2(RF_goal=0.9, DIM01=25, DIM02=2, DIM03=20, DIM04=15, stringer_pitch_in=200, thickness_skin_in=4, length=750, c=1, EModulus=65669.47, sigma_applied=-83.09)
    print(testopt_DIM2)
    testopt_DIM3 = reverseColumn_Euler_DIM3(RF_goal=0.9, DIM01=25, DIM02=2, DIM03=20, DIM04=15, stringer_pitch_in=200, thickness_skin_in=4, length=750, c=1, EModulus=65669.47, sigma_applied=-83.09)
    print(testopt_DIM3)
    testopt_thickness = reverseColumn_Euler_thickness_skin(RF_goal=0.9, DIM01=25, DIM02=2, DIM03=20, DIM04=15, stringer_pitch_in=200, thickness_skin_in=4, length=750, c=1, EModulus=65669.47, sigma_applied=-83.09)
    print(testopt_thickness)