from client import gc
from datetime import date
from flask import Flask 

app = Flask(__name__)

start_date = date(2019, 11, 15).toordinal()

sheet = gc.open("Sheet").sheet1
sheet.clear()

users = {}
users_count = 1
sheet.update_cell(1, 1, "DATE")

@app.route('/add_user/<name>')
def add_user(name):
	global users_count, users
	
	if name in users:
		return "User Already Exist"

	users_count = users_count + 1
	users[name] = users_count
	sheet.update_cell(1, users_count, name)
	return "User added"

@app.route('/mark/<name>')
def mark_attendence(name):
    global users, start_date

    if name not in users:
    	return "User does not Exist"
    col_index = users[name]
    curr_date = date.today() 	
    row_index = curr_date.toordinal() - start_date + 2

    sheet.update_cell(row_index, 1, curr_date.__str__() )
    sheet.update_cell(row_index, col_index, "Done")
    return "Attendence Marked"

app.run(host="0.0.0.0", port=5555)

# add_user("Ayush")
# add_user("Sachin")
# mark_attendence("Ayush", date(2019, 11, 18) )
# mark_attendence("Sachin", date(2019, 11, 18) )
# mark_attendence("Sachin", date(2019, 11, 22) )
# mark_attendence("Ayush", date(2019, 11, 23) )
