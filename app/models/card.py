from sqlalchemy.orm import backref
from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.String)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id', ondelete='cascade'))

    

    #do we want to use back populate or backref?
    #I think we want to do this:

    """
    One To Many
A one to many relationship places a foreign key on the child table referencing the parent. relationship() is then specified on the parent, as referencing a collection of items represented by the child:

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))



__________________________



To establish a bidirectional relationship in one-to-many, where the “reverse” side is a many to one, specify an additional relationship() and connect the two using the relationship.back_populates parameter:

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent", back_populates="children")
    
    
    """