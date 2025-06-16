import hm 
import hm.entities as ent

model = hm.Model()


#Offsets panel elements to the correct position
def updatePanelOffset(model, t1, t2, t3, t4, t5):
   """
   Here we shift the nodes of the individual panel elements 
   into the skin stringer intersection point 
   So by t_skin/downwards 
   """
   filter = hm.FilterByCollection(ent.Element, ent.Component)
   panels = hm.Collection(model, ent.Component, id="id=1,2,3,4,5,6,7,8,9,10")
   panelElements = hm.Collection(model,filter, panels)

   for element in panelElements:
        if element.component.name == 'panel1'
            element.zoff = t1/2
   return None


#Offsets stringer elements to the correct position
def updateStringerOffset(model):
    """
   Here we shift the nodes of the individual stringer elements 
   into the skin stringer intersection point
   So by the position of the elastic center upwards 
   """

    return None 



def changeParameters(model, skinThickness, columnDimensions):
    parameters = hm.Collection(model,ent.Parameter)
    for param in parameters:
        param.valuedouble = 4
    updatePanelOffset(model)
    updateStringerOffset(model)

