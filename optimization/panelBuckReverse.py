import math 



# Function for calculating the 
def reverseBiaxial(RF_goal, sigma_applied, k_bi, EModulus, nu, width):
    sigma_crit = abs(RF_goal * sigma_applied)
    thickness = width * math.sqrt(12* (sigma_crit/(k_bi*EModulus * math.pi**2)) * (1-nu**2))
    return thickness

def reverseShear(RF_goal, tau_applied, k_shear, EModulus, nu, width):
    tau_crit = abs(RF_goal*tau_applied)
    thickness = width * math.sqrt(12* (tau_crit/(k_shear*EModulus * math.pi**2)) * (1-nu**2))
    return thickness

def panelBuckReverse(row, EModulus, nu, RF_goal):
    # For biaxial we first need to check the principal direction 
    if row['sigmaYY'] < row['sigmaXX']: 
        #Swap stresses 
        sigma_appliedBi = row['sigmaYY']
        #swap dimensions
        widthBi = row['length']
    else:
        sigma_appliedBi = row['sigmaXX']
        widthBi = row['width']
    

    # Compute the reverse thicnesses 
    thicknessBi = reverseBiaxial(RF_goal=RF_goal, sigma_applied=sigma_appliedBi, k_bi=row['k_biaxial'], EModulus=EModulus, nu=nu, width=widthBi)
    thicknessShear = reverseShear(RF_goal=RF_goal, tau_applied=row['sigmaXY'], k_shear=row['k_shear'], EModulus=EModulus, nu=nu, width=row['width'])
    thickness = max(thicknessBi, thicknessShear)
    return thickness