import os
from SharePynt import SharePynt

sp = SharePynt("isweb.tyson.com","projects/BusinessSimulation","ntlm",10)
SPLib = "Supply Chain Order Tracking"
file = "C:/Shared/CORE - SC - STO.xlsx"
fileName = os.path.basename(file)

if SPLib != None and SPLib != "":
	sp.UploadFile(SPLib, fileName, file)