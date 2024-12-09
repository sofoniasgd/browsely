import os
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    location = Column(String)
    file_path = Column(String)
    root_dir_path = Column(String)

def scan_directory_and_add_to_db(root_dir, session):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(dirpath, filename)
                if dirpath[-3] == "w":
                    location = "woreda " + dirpath[-2:]
                elif dirpath[:5] == "KOLFE":
                    location = "Kolfe sub city"
                file_record = File(
                    name=filename,
                    location=location,
                    file_path=file_path,
                    root_dir_path=root_dir
                )
                print(file_record.name, file_record.location)
                # session.add(file_record)
    # session.commit()

def main():
    engine = db.create_engine('mysql+pymysql://browsely_sys:browsely_sys_pwd@localhost/browsely_db')

    Session = sessionmaker(bind=engine)
    session = Session()

    root_directory = '/mnt/c/Users/metasebia/Documents/projects/Searchly/test_directory'
    scan_directory_and_add_to_db(root_directory, session)

if __name__ == '__main__':
    main()