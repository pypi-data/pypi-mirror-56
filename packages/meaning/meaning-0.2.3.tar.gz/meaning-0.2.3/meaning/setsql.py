from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (Table, Column, Integer, Unicode, String, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///words.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Word(Base):
    __tablename__ = 'words'
    
    word_id = Column(Integer(), primary_key=True)
    word_name = Column(String(15), nullable=False, unique=True)
    word_count = Column(Integer(), nullable=False)
    word_translate = Column(Unicode(), nullable=False)
    create_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
       return "Word(word_name='{self.word_name}', "\
                    "word_count='{self.word_count}', "\
                    "word_translate='{self.word_translate}')".format(self=self)  

Base.metadata.create_all(engine)

def UpdateSQL(word: str, translate=None):
    if session.query(Word).filter(Word.word_name == word).first() :
        query = session.query(Word) 
        query = query.filter(Word.word_name == word) 
        query.update({Word.word_count: Word.word_count + 1}) 
        cc_word = query.first() 
    else:
        cc_word = Word(word_name=word,
                       word_count=1,
                       word_translate=translate)
    session.add(cc_word)
    session.commit()

def RecordsPromptShell():
    from terminaltables import SingleTable
    from sqlalchemy import desc

    data = []
    data.append(['word', 'translate', 'count', 'date'])
    for word in session.query(Word).order_by(desc(Word.updated_on)).limit(5):
        data.append([word.word_name, word.word_translate, word.word_count, word.updated_on])
    table = SingleTable(data)
    print(table.table)