import hm
import os 

#Constants
solver_template = "C:/Program Files/Altair/2025/hwdesktop/templates/feoutput/optistruct/optistruct"
file_path = "Test.fem"
solver_parameters = ["HM_NODEELEMS_SET_COMPRESS_SKIP ", "EXPORT_DMIG_LONGFORMAT ", "HMENGINEERING_XML", "HMSUBSYSTEMCOMMENTS_XML", "HMMATCOMMENTS_XML", "HMBOMCOMMENTS_XML", "INCLUDE_RELATIVE_PATH ", "EXPORT_SOLVER_DECK_XML_1 "]
#Run analysis
model = hm.Model()
model.hm_answernext("yes") #overwrite file if necessary 
model.feoutputwithdata(solver_template, file_path, 0,0,2, solver_parameters)

os.system(r'"C:\Program Files\Altair\2023.1\hwsolvers\scripts\optistruct.bat" Test.fem')

