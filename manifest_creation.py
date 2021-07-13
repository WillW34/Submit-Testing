# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 18:01:55 2020

@author: JVM
"""

import os, glob, mimetypes

host_address = "http://localhost:5000/public/"

cwd = os.getcwd()
path = os.path.join(cwd,'public','*')

file_list = glob.glob(path)


run_manifest = {"manifest":{"files":[]}}
for file in file_list:
  file_name = os.path.split(file)[1]
  file_type = mimetypes.guess_type(file_name)[0]
  file_url = host_address + file_name
  run_manifest['manifest']['files'].append({"url":file_url, "filename":file_name, "type":file_type})
  
  
run_manifest_str = str(run_manifest)
run_manifest_str = run_manifest_str.replace("'",'"')
  
with open(os.path.join(cwd,'run_manifest.txt'),'w') as file:
    file.write(run_manifest_str)