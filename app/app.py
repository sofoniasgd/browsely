from flask import Flask, request, jsonify, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import os

# Create the Flask app
app = Flask(__name__)
# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://browsely_sys:browsely_sys_pwd@localhost/browsely_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# define a class for the table
class Files(db.Model):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(20), nullable=False)
    location = Column(String(20), nullable=False)
    file_path = Column(String(255), nullable=False)
    root_directory = Column(String(255), nullable=False)

    def __repr__(self):
        return '<File %r>' % self.id

# Root endpoint to serve dashboard template
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# About endpoint for about page template
@app.route('/about')
def about():
    return render_template('about.html')
# pdf viewer endpoint
@app.route('/pdf_viewer')
def pdf_viewer():
    return render_template('pdf_viewer.html')

# Search endpoint that returns results of a MySQL query
@app.route('/search/<tin_number>')
def search(tin_number):
    # Query the database and return the results matching the tin number
    search_term = f'%{tin_number}%'
    print(search_term)
    result = Files.query.filter(Files.name.like(search_term)).all()
    if not result:
        return jsonify({'error': 'Data not found'})
    # Convert the results to a list of dictionaries
    result_json = []
    for record in result:
        result_json.append({
            'id': record.id,
            'name': record.name,
            'location': record.location,
            'file_path': record.file_path,
            'root_directory': record.root_directory
        })
    return jsonify(result_json)

# Download endpoint that returns a file
@app.route('/download/<file_name>')
def download(file_name):
    # Get the file path from the database
    file_record = Files.query.filter_by(name=file_name).first()
    file_path = file_record.file_path
    return send_file(file_path)


if __name__ == '__main__':
    app.run(debug=True)