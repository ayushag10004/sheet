from client import gc

sheet = gc.open("Sheet").sheet1

users = {}
users_count = 0

def add_user(name):
	global users_count, users
	users_count = users_count + 1
	users[name] = users_count
	sheet.update_cell(1, users_count, name)

sheet.clear()
add_user("Ayush")
add_user("Sachin")



# def mark_attendence(name, date):
# 	col_index = users[name]

