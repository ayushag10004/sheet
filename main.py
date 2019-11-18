from client import gc
from datetime import date
from flask import Flask 
import threading 
import time
import copy
from gspread_formatting import *
from flask import send_file

def background(f):
    '''
    a decorator to run function in background
    use @background above the function you want to run in the background
    '''

    def bg_f(*a, **kw):
        # Capturing the exception whenever thread dies
        try:
            threading.Thread(target=f, args=a, kwargs=kw).start()
        except:
            pass

    return bg_f

app = Flask(__name__)

start_date = date(2019, 11, 12).toordinal()

sheet = gc.open("Sheet").sheet1
sheet.clear()

users = {}
users_count = 1
default_format = CellFormat(backgroundColor=color(1, 1, 1), textFormat=textFormat(bold=True))
format_cell_range(sheet, rowcol_to_a1(1, 1)+':' + rowcol_to_a1(1000, 26), default_format)
sheet.update_cell(1, 1, "DATE")

fmt = cellFormat(
    backgroundColor=color(1, 0, 1),
    textFormat=textFormat(bold=True, foregroundColor=color(0, 0, 0)),
    horizontalAlignment='CENTER'
    )

cell_formats = {}

@app.route('/add_user/<name>')
def add_user(name):
	global users_count, users, fmt, cell_formats
	
	if name in users:
		return "User Already Exist"

	users_count = users_count + 1

	user_fmt = copy.deepcopy(fmt)
	dx = 0.3*users_count

	user_fmt.backgroundColor.red = user_fmt.backgroundColor.red - dx
	user_fmt.backgroundColor.green = user_fmt.backgroundColor.green + dx
	user_fmt.backgroundColor.blue = user_fmt.backgroundColor.blue - 0.5*dx
	cell_formats[name] = user_fmt

	users[name] = users_count
	sheet.update_cell(1, users_count, name)
	return "User added"

@app.route('/mark/<name>')
def mark_attendence(name):
    global users, start_date, cell_formats

    if name not in users:
    	return "User does not Exist"

    col_index = users[name]
    curr_date = date.today() 	
    row_index = curr_date.toordinal() - start_date + 1

    user_fmt = cell_formats[name]
    format_cell_range(sheet, rowcol_to_a1(row_index, col_index)+':' + rowcol_to_a1(row_index, col_index), user_fmt)
    sheet.update_cell(row_index, 1, curr_date.__str__() )
    sheet.update_cell(row_index, col_index, "Done")

    return "Attendence Marked"

app.run(host="0.0.0.0", port=5555)

@background
def run_daily_job():
	while(1):
		curr_date = date.today() 	
		row_index = curr_date.toordinal() - start_date + 1
		sheet.update_cell(row_index, 1, curr_date.__str__() )
    	
		for i in range(users_count):
			sheet.update_cell(row_index, i + 2, "*")
			format_cell_range(sheet, rowcol_to_a1(row_index, i+2)+':' + rowcol_to_a1(row_index, i+2), fmt)

		time.sleep(86400)

# run_daily_job()

# threading.Thread(target=run_daily_job).start()

# add_user("Ayush")
# add_user("Sachin")
# mark_attendence("Ayush", date(2019, 11, 18) )
# mark_attendence("Sachin", date(2019, 11, 18) )
# mark_attendence("Sachin", date(2019, 11, 22) )
# mark_attendence("Ayush", date(2019, 11, 23) )
