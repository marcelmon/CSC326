
<html>
	<body>

		<form action="" method="get">
			<input type="text" name="keywords"></input>
			<input type="submit" name="submit_query" value="Submit"></input>
		</form>
		%if Tuples_List != None and Tuples_List.length > 0
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

		%if Results_List != None and Results_List.length > 0
		<div>
			Results Table
			<table name="results">

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
</html>