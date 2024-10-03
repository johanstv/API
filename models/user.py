from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine


users = Table("Usuarios", meta, Column(
    "id", Integer, primary_key=True),
     Column("Nombre", String(255)),
     Column("Email", String(255)),
     Column("Direccion", String(255)),
     Column("Edad", Integer),
     )

meta.create_all(engine)