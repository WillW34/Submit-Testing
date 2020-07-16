from flask import Flask
import os, flask

app = Flask(__name__)

@app.route("/status")
def status():
    return("The Server Test Plugin Flask Server is up and running")

@app.route("/public/<file_name>")
def success(file_name):
    cwd = os.getcwd()
    path = os.path.join(cwd,'public')
    try:
        return flask.send_from_directory(path,file_name)
    except:
        with open(os.path.join(cwd,"Static_File_Not_Found.html")) as file:
            error_message = file.read()
            
        error_message = error_message.replace('REPLACE_FILENAME',file_name)
        return error_message, 404
        
