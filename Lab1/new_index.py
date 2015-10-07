
import os
from cStringIO import StringIO
from bottle import route, run, template
import pickle



@route('/new_index')
def new_index():
	#query_count = Query_Counter()

	queryForm = '<form action="/index/submit_query" method="post" name="query_form"><input type="textline" name="query_textline"/><input type="submit" name="query_submit" value="submit"/></form>'
		
	if not action or action == '':

		return '<html>'+query_form +'<div>' + Get_Dictionary_HTML(query_count.dictionary)+'</div></html>'

	else:
		if action == 'submit_query':
			if isinstance(query_count.dictionary, dict):
				value_text = request.forms.get('query_textline')
				if not value_text == None and value_text != '':
					return '<html>' + queryForm + '</html>'

				else:
					return '<html>' + queryForm + '<div>' + query_count.Process_Text(value_text) + '</div></html>'


	return '<html>'+queryForm +'<div>' #+ Get_Dictionary_HTML(query_count.dictionary)+'</div></html>'


run(host='localhost', port=8080, debug=True)