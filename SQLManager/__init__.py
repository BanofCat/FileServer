from flask_sqlalchemy import SQLAlchemy
from SQLManager.RelationalTableObject.BaseModel import BaseModel

sql_object = SQLAlchemy(model_class=BaseModel)
