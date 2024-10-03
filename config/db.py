from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:123456@localhost:3306/api")

meta = MetaData()

conn = engine.connect()


