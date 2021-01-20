#!/usr/bin/python

import http.server

import socketserver
import re
import io
import cgi
import os
import local_operators
import json
import base64
from base64 import encodebytes
from PIL import Image
#import SimpleHTTPServer

PORT = 9090
FORM_KEY = "image"

def get_response_image(image_path):
	pil_img = Image.open(image_path, mode='r') # reads the PIL image
	byte_arr = io.BytesIO()
	pil_img.save(byte_arr, format='JPEG') # convert the PIL image to byte array
	encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
	
	return encoded_img


class CustomHandler(http.server.SimpleHTTPRequestHandler):

	def do_POST(self):
		if None != re.search('/poc-doc/recognise*', self.path):
			status, image_path, category = self.deal_post_data()
		
			
			# writing response to app that called API
			
			f = io.BytesIO()
			
			#if r:
			#	f.write(b"Success\n")
			#else:
			#	f.write(b"Failed\n")
			
			#length = f.tell()
			#f.seek(0)
			
			f.write(json.dumps({'status': status, 'imageBytes': get_response_image(image_path), 'category': category}).encode())
			
			length = f.tell()
			f.seek(0)
			
			self.send_response(200)
			self.send_header("Content-type", "application/json")
			self.send_header("charset", "utf-8")
			self.send_header("Content-Length", str(length))
			self.end_headers()
			
			if f:
				self.copyfile(f, self.wfile)
				f.close()
				
			# proof - when decoded from base64 to binary (ONLY .jpg images work!!!!) - is displayed as image
			#im = Image.open(io.BytesIO(base64.b64decode(get_response_image(image_path))))
			#im.save('image1.jpg', 'JPEG')
			
			return
		else:
			#serve files, and directory listings by following self.path from
			#current working directory
			SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
	
	
	# shranjevanje slike na strezniku
	def deal_post_data(self):
		ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
		pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
		pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
		
		SAVE_PATH = "./images"
		STATUS = False
		RES_PATH = ""
		RES_CATEGORY = ""
		
		if ctype == 'multipart/form-data':
			form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
			# print("input: ", form[FORM_KEY])
			try:
				#if isinstance(form[FORM_KEY], list):
				#	for record in form[FORM_KEY]:
				#		FILE_NEW_NAME = str(len([name for name in os.listdir(SAVE_PATH) if os.path.isfile(os.path.join(SAVE_PATH, name))]))
				#		FULL_NAME = os.path.join(SAVE_PATH, FILE_NEW_NAME)	#record.filename
				#		open(FULL_NAME, "wb").write(record.file.read())
				#else:
				FILE_NEW_NAME = str(len([name for name in os.listdir(SAVE_PATH) if os.path.isfile(os.path.join(SAVE_PATH, name))]))
				FULL_NAME = os.path.join(SAVE_PATH, FILE_NEW_NAME + ".jpg")		#form[FORM_KEY].filename
				SAVE_RESULT_PATH = "images_res"
				
				open(FULL_NAME, "wb").write(form[FORM_KEY].file.read())
				#open(FULL_NAME, "wb").write(io.BytesIO(base64.b64decode(form[FORM_KEY])))

				RES_PATH, RES_CATEGORY = local_operators.locate_object(FULL_NAME, "predict_set", "model", 128, SAVE_RESULT_PATH)
				STATUS = True
				
			except IOError:
					return (False, "Can't create file to write, do you have permission to write?")
		return (STATUS, RES_PATH, RES_CATEGORY)

			
if __name__=='__main__':
	httpd = socketserver.TCPServer(("", PORT), CustomHandler)
	print("Serving on 0.0.0.0:", PORT, " ...")
	httpd.serve_forever()
