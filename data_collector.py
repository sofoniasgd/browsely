import os
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    location = Column(String(20), nullable=False)
    file_path = Column(String(255), nullable=False)
    root_directory = Column(String(255), nullable=False)

def scan_directory_and_add_to_db(root_dir, session):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(dirpath, filename)
                # print(file_path)
                if dirpath[-3] == "w":
                    location = "woreda " + dirpath[-2:]
                elif dirpath[-14:] == "KOLFE E-FILING":
                    location = "Kolfe_sub_city"
                else:
                    location = 'not_specified'
                
                # blacklisted directories
                blacklisted_directories = ['woreda 01', 'not_specified']

                # skip if location is not specified or within the blacklisted directories
                if location in blacklisted_directories:
                    continue

                file_record = File(
                    name=filename,
                    location=location,
                    file_path=file_path,
                    root_directory=root_dir
                )
                print("adding file: {} || {}\n{}".format(file_record.name, file_record.location, file_record.file_path))
                session.add(file_record)
    session.commit()

def main():
    engine = db.create_engine('mysql+pymysql://browsely_sys:browsely_sys_pwd@localhost/browsely_db')

    Session = sessionmaker(bind=engine)
    session = Session()

    root_directory = '/mnt/c/Users/metasebia/Documents/projects/Browsely/test_directory'
    scan_directory_and_add_to_db(root_directory, session)

if __name__ == '__main__':
    main()