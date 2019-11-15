from client import gc
from datetime import date

start_date = date(2019, 11, 15).toordinal()

sheet = gc.open("Sheet").sheet1
sheet.clear()

users = {}
users_count = 1
sheet.update_cell(1, 1, "DATE")

def add_user(name):
	global users_count, users
	users_count = users_count + 1
	users[name] = users_count
	sheet.update_cell(1, users_count, name)

def mark_attendence(name, date):
    global users, start_date
    col_index = users[name]
    curr_date = date.toordinal() 	
    row_index = curr_date - start_date + 1
    sheet.update_cell(row_index, 1, date.__str__() )
    sheet.update_cell(row_index, col_index, "Done")

add_user("Ayush")
add_user("Sachin")
mark_attendence("Ayush", date(2019, 11, 18) )
mark_attendence("Sachin", date(2019, 11, 18) )
mark_attendence("Sachin", date(2019, 11, 22) )
mark_attendence("Ayush", date(2019, 11, 23) )


# def mark_attendence(name, date):
# 	col_index = users[name]

