#!/usr/bin/python
# coding: utf-8

import flask
import mangaScrape
from webapp import app
import re

# importing application wide parameters and global variables that have been
# defined in __init__.py

@app.route('/', methods=('GET','POST'))
def webapp():
	url=""
	pages=""
	folder=""
	if flask.request.method=='POST':
		url = flask.request.form.get('url')
		pages = flask.request.form.get('pages')
		folder=re.split(r"/", url)[3] + "_"+re.split(r"/", url)[4]
		mangaScrape.main(url, folder, int(pages))
	return flask.render_template('index.html', url=url, 
					pages=pages)
@app.route('/about/')
def about():
    return flask.render_template('about.html')
@app.route('/contact/')
def contact():
    return flask.render_template('contact.html', yo="pp")
