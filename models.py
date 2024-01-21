from sqlalchemy import Integer, Boolean, String, Column, Text
from database import Base

class Item(Base):
    __tablename__='items2'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique = True)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    on_offer = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Item name={self.name}, price = {self.price}>"