import sqlite3

conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS TODO(task TEXT,status TEXT,to_date DATE,PRIMARY KEY(task))')

def add_data(task,status,to_date):
	c.execute('INSERT INTO  TODO(task,status,to_date) VALUES (?,?,?)',(task,status,to_date))
	conn.commit()

def view_data():
	c.execute('SELECT * FROM TODO')
	data = c.fetchall()
	return data

def view_task():
	c.execute('SELECT DISTINCT task FROM TODO')
	data = c.fetchall()
	return data

def get_task(task):
	c.execute('SELECT * FROM TODO WHERE task="{}"'.format(task))
	data = c.fetchall()
	return data

def edit(new_task,new_status,new_to_date,task,status,date):
	c.execute('UPDATE TODO SET task=?,status=?,to_date=? WHERE task=? and status=? and to_date=?',(new_task,new_status,new_to_date,task,status,date))
	conn.commit()
	data = c.fetchall()
	return data	

def delete(task):
	c.execute('DELETE FROM TODO WHERE task="{}"'.format(task))
	conn.commit()