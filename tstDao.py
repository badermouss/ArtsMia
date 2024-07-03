from database.DAO import DAO
from model.model import Model

model = Model()
model.creaGrafo()

res = DAO.getAllObjects()

conn = DAO.getAllConnessioni(model._idMap)

print(len(conn))
print(len(res))
