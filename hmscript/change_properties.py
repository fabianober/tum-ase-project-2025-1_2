import hm 
import hm.entities as ent

model = hm.Model()


#Offsets panel elements to the correct position
def updatePanelOffset(model):
   """
   Here we shift the nodes of the individual panel elements 
   into the skin stringer intersection point 
   So by t_skin/downwards 
   """
   return None


#Offsets stringer elements to the correct position
def updateStringerOffset(model):
    """
   Here we shift the nodes of the individual stringer elements 
   into the skin stringer intersection point
   So by the position of the elastic center upwards 
   """
    return None 



def changeParameters(model):
    parameters = hm.Collection(model,ent.Parameter)
    for param in parameters:
        param.valuedouble = 4
    updatePanelOffset()
    updateStringerOffset()

