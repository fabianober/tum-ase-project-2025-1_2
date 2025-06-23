import hm 
import hm.entities as ent

model = hm.Model()

#Change the panel Thickness
def changePanelThickness(panelThickness):
    parameters = hm.Collection(model, ent.Parameter)
    #print("Changing panel thickness")
    for param in parameters:
        if param.name == 'panelT1':
            param.valuedouble = panelThickness[0]
            #print(panelThickness[0])
        elif param.name == 'panelT2' :
            param.valuedouble = panelThickness[1]
        elif param.name =='panelT3' :
            param.valuedouble = panelThickness[2]
        elif param.name == 'panelT4' or param.name == 'Shell7':
            param.valuedouble = panelThickness[3]
        elif param.name == 'panelT5':
            param.valuedouble = panelThickness[4]
    return None


#Offsets panel elements to the correct position
def updatePanelOffset(skinThickness):
   """
   Here we shift the nodes of the individual panel elements 
   into the skin stringer intersection point 
   So by t_skin/downwards 
   """
   filter = hm.FilterByCollection(ent.Element, ent.Component)
   panels = hm.Collection(model, ent.Component, id="1,2,3,4,5,6,7,8,9,10")
   panelElements = hm.Collection(model,filter, panels)

   for element in panelElements:
        if element.component.name == 'panel1' or element.component.name == 'panel10':
            element.ZOFFS = skinThickness[0]/2
        elif element.component.name == 'panel2' or element.component.name == 'panel9':
            element.ZOFFS = skinThickness[1]/2
        elif element.component.name == 'panel3' or element.component.name == 'panel8':
            element.ZOFFS = skinThickness[2]/2
        elif element.component.name == 'panel4' or element.component.name == 'panel7':
            element.ZOFFS = skinThickness[3]/2
        elif element.component.name == 'panel5' or element.component.name == 'panel6':
            element. ZOFFS = skinThickness[4]/2
   return None




def changeStringerDimensions(stringerDim):
    beamsects = hm.Collection(model, ent.Beamsection)
    for beamsect in beamsects:  
        if beamsect.name == 'Stringer_Section1' or beamsect.name == 'Stringer_Section9':
            beamsect.beamsect_dim1 = stringerDim[0][0]
            beamsect.beamsect_dim2 = stringerDim[0][1]
            beamsect.beamsect_dim3 = stringerDim[0][2]
            beamsect.beamsect_dim4 = stringerDim[0][3]
        elif beamsect.name == 'Stringer_Section2' or beamsect.name == 'Stringer_Section8':
            beamsect.beamsect_dim1 = stringerDim[1][0]
            beamsect.beamsect_dim2 = stringerDim[1][1]
            beamsect.beamsect_dim3 = stringerDim[1][2]
            beamsect.beamsect_dim4 = stringerDim[1][3]
        elif beamsect.name == 'Stringer_Section3' or beamsect.name == 'Stringer_Section7':
            beamsect.beamsect_dim1 = stringerDim[2][0]
            beamsect.beamsect_dim2 = stringerDim[2][1]
            beamsect.beamsect_dim3 = stringerDim[2][2]
            beamsect.beamsect_dim4 = stringerDim[2][3]
        elif beamsect.name == 'Stringer_Section4' or beamsect.name == 'Stringer_Section6':
            beamsect.beamsect_dim1 = stringerDim[3][0]
            beamsect.beamsect_dim2 = stringerDim[3][1]
            beamsect.beamsect_dim3 = stringerDim[3][2]
            beamsect.beamsect_dim4 = stringerDim[3][3]
        elif beamsect.name == 'Stringer_Section5':
            beamsect.beamsect_dim1 = stringerDim[4][0]
            beamsect.beamsect_dim2 = stringerDim[4][1]
            beamsect.beamsect_dim3 = stringerDim[4][2]
            beamsect.beamsect_dim4 = stringerDim[4][3]
    
    return None

#Offsets stringer elements to the correct position
def updateStringerOffset():
    """
   Here we shift the nodes of the individual stringer elements 
   into the skin stringer intersection point
   So by the position of the elastic center upwards 
   """
    # Get the corresponding stringer elements 
    filter = hm.FilterByCollection(ent.Element, ent.Component)
    stringers = hm.Collection(model, ent.Component, id="id=11,12,13,14,15,16,17,18,19")
    stringerElements = hm.Collection(model,filter, stringers)

    #The offset we get from the beam sections 
    beamsections = hm.Collection(model, ent.Beamsection)
    stringerOffset = []
    for beamsect in beamsections:
        if 'Stringer' in beamsect.name: 
            stringerOffset.append(-round(beamsect.results_coordExt0,3))
    
    # Now we apply this offset 
    for element in stringerElements:
        if element.component.name == 'stringer1' or element.component.name == 'stringer9':
            element.offsetaz = stringerOffset[0]
            element.offsetbz = stringerOffset[0] 
        elif element.component.name == 'stringer2' or element.component.name == 'stringer8':
            element.offsetaz = stringerOffset[1]
            element.offsetbz = stringerOffset[1]
        elif element.component.name == 'stringer3' or element.component.name == 'stringer7':
            element.offsetaz = stringerOffset[2]
            element.offsetbz = stringerOffset[2]
        elif element.component.name == 'stringer4' or element.component.name == 'stringer6':
            element.offsetaz = stringerOffset[3]
            element.offsetbz = stringerOffset[3] 
        elif element.component.name == 'stringer5' :
            element.offsetaz = stringerOffset[4]
            element.offsetbz = stringerOffset[4] 
    return None 


def changeParameters(skinTickness, stringerDim):
    changePanelThickness(skinTickness) #update panel Dimensions (array of 5 thicknesses)
    changeStringerDimensions(stringerDim)  #update stringer dimensions (list within list, (Dim1: height, Dim2; thickness, Dim3: "head" width, Dim4: length of Omega 'legs'))
    updatePanelOffset(skinTickness)
    updateStringerOffset()