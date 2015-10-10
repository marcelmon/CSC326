


import os
from cStringIO import StringIO

from bottle import request, route, run, template
import pickle


def Load_And_Unserialize(file_name):

	if os.path.exists(file_name):
		if os.path.isfile(file_name):
			fp = open(file_name, 'r')
			serialized_counter = fp.read()
			fp.close()

			new_Counter = pickle.loads(serialized_counter)
		 	if isinstance(new_Counter, New_Query_Counter):
				return new_Counter
	return -1

def Serialize_And_Store(file_name, counter_object):
	if os.path.exists(file_name):
		if not os.path.isfile(file_name):
			return -1

	serialized_counter = pickle.dumps(counter_object)
	fp = open(file_name, 'w')
	fp.write(serialized_counter)
	fp.close()

	return 1


def Get_List_Index(the_list, word):
	for index, list_word in enumerate(the_list):
		if list_word == word:
			#is in list
			return index
	return -1


def Swap_In_List(the_list, index_1, index_2):
	the_list[index_1], the_list[index_2] = the_list[index_2], the_list[index_1]
	return the_list


class New_Query_Counter(object):

	"""docstring for """

	word_count_table = {}

	top_20_list = []
	top_20_list_count = 0;

	def __init__(self):
		self.word_count_table = {}
		self.top_20_list = []





	def Get_Top_20_Tuples(self):
		return_list = []

		for word in self.top_20_list:
			count = self.word_count_table[word]
			return_list.append( (word, count) )

		return return_list

	def Process_Query(self, query_string):

		word_array = query_string.split()
		this_word_count = {}

		for word in word_array:
			if word in this_word_count:
				this_word_count[word] += 1
			else:
				this_word_count[word] = 1

		
		for word, add_count in this_word_count.iteritems():
			self.Add_Word_Count(word, add_count)

			if self.Bubble_Top_20_List(word, self.word_count_table[word]) == -22:
				return -22

		return list(this_word_count.items())

	def Add_Word_Count(self, word, add_count):
		if  self.word_count_table.get(word) == None:
			self.word_count_table[word] = add_count
		else:
			self.word_count_table[word] += add_count
		return

	def Bubble_Top_20_List(self, word, count):

		index = Get_List_Index(self.top_20_list, word)
		this_count = self.word_count_table[word]

		if index == 0:
			#no need to do anything
			return

		elif index == -1:
			#automatically append word if list length is less than MAX
			length = len(self.top_20_list)
			if length < 20:
				self.top_20_list.append(word)
				index = length

			#else first check if the word can at least be added as the last word
			else:
				last_count = self.word_count_table[self.top_20_list[length-1]]
				if this_count > last_count:
					self.top_20_list[length-1] = word
					index = length - 1
				else:
					return

		#continue to bubble element from the end until it reaches the front or is not greater
		while index > 0:


			next_count = self.word_count_table[self.top_20_list[index-1]]

			if this_count > next_count:
				Swap_In_List(self.top_20_list, index, index-1)
				index -= 1
			else:
				return
			
		return



@route('/index', method='GET')
def index():
	Query_Counter = Load_And_Unserialize('the_counter.txt')

	if Query_Counter == -1:
		Query_Counter = New_Query_Counter()

	query = request.query.keywords

	if query == None or len(query) ==0 :
		top_20_tuples = Query_Counter.Get_Top_20_Tuples()
		Serialize_And_Store('the_counter.txt', Query_Counter)
		return template(front_template, Results_List=None, Tuples_List=top_20_tuples)

	else:
		query_results = Query_Counter.Process_Query(query)
		if query_results == -22:
			return 'DAFUNKLES'

		top_20_tuples = Query_Counter.Get_Top_20_Tuples()
		Serialize_And_Store('the_counter.txt', Query_Counter)
		return template(front_template, Results_List=query_results, Tuples_List=top_20_tuples)



front_template= """
<html>
	<body>

		<form action="" method="get">
			<input type="text" name="keywords"></input>
			<input type="submit" name="submit_query" value="Submit"></input>
		</form>
		%if Tuples_List != None and len(Tuples_List) > 0:
		<div>
		History Table
			<table name="history">
				<tr>
					<td>
						Word
					</td>
					<td>
						Count
					</td>
				</tr>
				%for word,count in Tuples_List:
				<tr>
					<td>
						{{word}}
					</td>
					<td>
						{{count}}
					</td>
				</tr>
				%end
			</table>
		</div>
		%end

		%if Results_List != None and len(Results_List) > 0:
		<div>
			Results Table
			<table name="results">
				<tr>
					<td>
						Word
					</td>
					<td>
						Count
					</td>
				</tr>
				%for word,count in Results_List:
				<tr>
					<td>
						{{word}}
					</td>
					<td>
						{{count}}
					</td>
				</tr>
				%end
			</table>
		</div>
		%end
	</body>
</html>"""


if __name__ == '__main__':
	new_counter_object = New_Query_Counter();
	Serialize_And_Store('the_counter.txt', new_counter_object);

	port = int(os.environ.get('PORT', 8080))
	run(host='localhost', port=port, debug=True)








# @route('/index')
# def hello():

# 	query_count = Query_Counter()
# 	queryForm = '<form action="/submit_query" method="post" name="query_form"><input type="text" name="queryTextline"/><input type="submit" name="query_submit" value="submit"/></form>'

# 	return '<html>'+queryForm +'<div>' + Get_Dictionary_HTML(query_count.dictionary)+'</div></html>'


# @route('/submit_query', method='POST')
# def new_hello():

# 	#constructor of query_counter will check for the file, or create one if needed
# 	query_count = Query_Counter()
# 	queryForm = '<form action="/submit_query" method="post" name="query_form"><input type="textline" name="queryTextline"/><input type="submit" name="query_submit" value="submit"/></form>'
	

# 	if isinstance(query_count.dictionary, dict):

# 		value_text = request.forms.get('queryTextline')

# 		if value_text == None or value_text == '':
# 			return queryForm

# 		else:
# 			returnText = query_count.Process_Text(value_text)
# 			query_count.pack_up()

# 			return queryForm + '<div>' + returnText + '</div>'
# 	else:
# 		return '<html><div>There was an Error</div>' + queryForm + '</html>'


# class Query_Counter(object):
# 	"""Object for handling data interface requests"""

# 	dictionary = {}
# 	top_20_dict = {}

# 	def __init__(self):
# 		if os.path.exists('Query_Counter.txt'):
# 			if os.path.isfile('Query_Counter.txt'):

# 				fp = open('Query_Counter.txt', 'r')
# 				new_self_txt = fp.read()
# 				fp.close()

# 				if new_self_txt == None or new_self_txt == '':
# 					self.dictionary = {}
# 					self.top_20 = {}
# 					return self

# 				else:
# 					new_self = pickle.loads(new_self_txt)
# 				 	if isinstance(new_self, Query_Counter):
# 						self = new_self


# 	def pack_up(self):
# 		"""Save the object"""

# 		fp = open('Query_Counter.txt', 'w+')
# 		fp.write(pickle.dumps(self))
# 		fp.close()



# 	def Process_Text(self, txt):
# 		"""Input text from the text line, split, remove whitespace, and add to dictionary"""
# 		new_text = txt.split()

# 		this_word_count = {}

# 		for t in new_text:
# 			text = t.strip()
# 			Add_Dictionary_Count(self.dictionary, text)
# 			self.Test_Is_Top_20(text)

# 			if this_word_count.has_key(text) and this_word_count[text] != None and this_word_count[text] > 0:
# 				this_word_count[text] += 1
# 			else:
# 				this_word_count[text] = 1


# 		this_count_table = Get_Dictionary_HTML(this_word_count)

# 		html = '<div style="align:centre">Search for: '+ txt + this_count_table+'</div>'

# 		html += '<div style="align:center">Top 20 Search Words: '+ Get_Dictionary_HTML(self.dictionary)+'</div>'

# 		return html



# 	def Test_Is_Top_20(self, word):
# 		"""keep separate list of top 20 for optimization
# 		check if word is in dictionary, see if count is greater than the least in dictionary"""
# 		if not isinstance(self.top_20_dict, dict):
# 			return 'Error not dict'

# 		if not isinstance(self.dictionary, dict):
# 			return 'Error not dict'
# 		#this needs to be changed, need to take first element of the top 20 dictionay
# 		lowest = 99999999999999
# 		lowest_string = ''

# 		new_top_20_dict = {}

# 		if self.dictionary.has_key(word) and self.dictionary[word] != None and self.dictionary[word] > 0:

# 			#the word is already in the top_20_dict
# 			if self.top_20_dict.has_key(word) and self.top_20_dict[word] != None and self.top_20_dict[word] > 0:
# 				new_top_20_dict = self.top_20_dict
# 				new_top_20_dict[word] += 1

# 			else:
# 				curr_count = 0

# 				#count number of items not None and find the lowest count
# 				for the_word,count in self.dictionary.iteritems():
# 					if the_word != None and count != None and count > 0:
# 						curr_count += 1

# 						new_top_20_dict[the_word] = count
# 						if count < lowest:
# 							lowest = count
# 							lowest_string = the_word

# 				#there are less than 20 items not set to none or 0, so just add
# 				if curr_count < 20:
# 					new_top_20_dict[word] = 1

# 				#lowest is less than the current checking word count, so replace
# 				else:
# 					if lowest < self.dictionary[word]:
# 						new_top_20_dict[lowest_string] = None
# 						new_top_20_dict[word] = self.dictionary[word]
# 				#else lowest is equal or greater than the count of checking word
# 		else:
# 			return top_20_dict

# 		self.top_20_dict = new_top_20_dict

# 		return self.top_20_dict




# def Get_Dictionary_HTML(dictionary):
# 	"""Return html table of dictionary"""
# 	if not isinstance(dictionary, dict):
# 		return 'Error not a dictionary'

# 	return_string = '<table><tr><td>Word</td><td>Count</td></tr>'

# 	for word, count in dictionary.iteritems():
# 		return_string += '<tr><td>' + word + '</td><td>' + str(count) + '</td></tr>'

# 	return_string += '</table>'
# 	return return_string



# def Add_Dictionary_Count(dictionary, word):
# 	"""Find word in dictionary, increment value"""
# 	if dictionary.has_key(word):
# 		if dictionary[word] != None and dictionary[word] > 0:
# 			dictionary[word] += 1
# 		else:
# 			dictionary[word] = 1
# 	else:
# 		dictionary[word] = 1



# run(host='localhost', port=8080, debug=True)