from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib

# 数据库的配置变量
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'ftp'
USERNAME = 'root'
PASSWORD = 'password'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
# 创建数据库引擎
engine = create_engine(DB_URI)

Base = declarative_base(engine)

session = sessionmaker(bind=engine)()



class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    _password = Column(String(200), nullable=False)


    def __init__(self, username, password):
        self.username = username
        self.password = password


    @property
    def password(self):
        return self._password


    @password.setter
    def password(self, raw_password):
        raw_password = bytes(raw_password, encoding='utf8')
        self._password =hashlib.new('md5', raw_password).hexdigest()


    def check_password(self, input):
        input_password = hashlib.new('md5', bytes(input, encoding='utf8'))
        return self._password == input_password.hexdigest()



# Base.metadata.create_all()






