import hm 
import hm.entities as ent

model = hm.Model()

parameters = hm.Collection(model,ent.Parameter)


for param in parameters:
    param.valuedouble = 4

