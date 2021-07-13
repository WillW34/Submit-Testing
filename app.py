from flask import Flask, request, send_from_directory,send_file
import os
import sys
import requests
import shutil
import zipfile

sys.path.insert(0,'shortbol')
from shortbol import run as shb_run
shortbol_libs = os.path.join("shortbol", "templates")
tempdir = "tempdir"
out_dir = "outdir"
app = Flask(__name__)

@app.route("/status")
def status():
    return("The Server Test Plugin Flask Server is up and running")

@app.route("/public/<file_name>")
def success(file_name):
    cwd = os.getcwd()
    path = os.path.join(cwd,'public')
    try:
        return send_from_directory(path,file_name)
    except:
        with open(os.path.join(cwd,"Static_File_Not_Found.html")) as file:
            error_message = file.read()
            
        error_message = error_message.replace('REPLACE_FILENAME',file_name)
        return error_message, 404
        

@app.route("/run", methods=["POST"])
def run():    
    input_manifest = request.get_json(force=True)
    output_manifest = {"results":[]}
    files = input_manifest['manifest']['files']
    _setup_dirs()
    for file in files:
        f_loc = file["url"]
        fn = file["filename"]
        response = requests.get(f_loc)
        assert(response.status_code == 200)
        sbh_input = os.path.join(tempdir,"temp_shb.txt")
        out_fn = fn.split(".")[0] + ".xml"
        sbol_out = os.path.join(out_dir, out_fn)
        with open(sbh_input,"w") as sbh_file:
            sbh_file.write(response.text)
        shb_run.parse_from_file(sbh_input, out=sbol_out, optpaths=[shortbol_libs])
        output_manifest["results"].append({"filename":out_fn,"sources":[fn]})
    _write_manifest(output_manifest)
    out_zip = _make_archive(out_dir)
    _cleanup()
    return send_file(out_zip)


def _setup_dirs():
    if os.path.isdir(tempdir):
        shutil.rmtree(tempdir)
    os.mkdir(tempdir)

    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)
def _cleanup():
    if os.path.isdir(tempdir):
        shutil.rmtree(tempdir)
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)

def _make_archive(source):
    destination = source + ".zip"
    shutil.make_archive(source, "zip", source)
    shutil.move('%s.%s'%(source,"zip"), destination)
    return destination

def _write_manifest(manifest):
    file_path_out = os.path.join(out_dir, "manifest.json")
    with open(file_path_out, 'w') as manifest_file:
            manifest_file.write(str(manifest)) 
