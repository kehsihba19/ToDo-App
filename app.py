import streamlit as st
import pandas as pd 
from data import create_table,add_data,view_data,view_task,get_task,edit,delete
from datetime import date 
import streamlit.components.v1 as stc
HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">ToDo App</h1>
    </div>
    """

def main():
	stc.html(HTML_BANNER)
	menu=['Create','Read','Update','Delete']
	choice=st.sidebar.selectbox("Menu",menu)
	create_table()
	if choice=='Create':
		st.subheader("Add Items")
		col1,col2=st.beta_columns(2)
		with col1:
			task=st.text_area("Task To Do")
		with col2:
			status=st.selectbox("Status",["ToDo","Doing","Done"])
			to_date=st.date_input("Due Date")
		if st.button("Add Task"):
			if(task==''):
				st.warning('Enter the task first')
			elif(len(get_task(task))):
				st.error('Task already exists')
			else:
				add_data(task,status,to_date)
				st.success("Added Task :: {}".format(task))

	elif choice=='Read':
		data = view_data()
		sf = pd.DataFrame(data,columns=["Task","Status","Due Date"])
		with st.beta_expander("View All"):
			st.dataframe(sf)
		with st.beta_expander("Task Status"):
			task = sf["Status"].value_counts().to_frame()
			task=task.reset_index()
			st.dataframe(task)

	elif choice=='Update':
		st.subheader("Edit/Update Items")
		data = view_data()
		sf = pd.DataFrame(data,columns=["Task","Status","Due Date"])
		with st.beta_expander("Current data"):
			st.dataframe(sf)

		list_of_tasks = [i[0] for i in view_task()]
		selected_task = st.selectbox("Task",list_of_tasks)
		task_result = get_task(selected_task)

		if task_result:
			task = task_result[0][0]
			task_status = task_result[0][1]
			task_to_date = task_result[0][2]
			date_val=task_to_date.split('-')
			date_val=[int(x) for x in date_val]
			task_to_date=date(date_val[0],date_val[1],date_val[2])

			task_list=["ToDo","Doing","Done"]
			task_index=task_list.index(task_status)
			col1,col2 = st.beta_columns(2)
			
			with col1:
				new_task = st.text_area("Task To Do",task)

			with col2:
				new_task_status = st.selectbox("Status",task_list,index=task_index)
				new_task_to_date = st.date_input("Due Date",task_to_date)
			if st.button("Update Task"):
				if(new_task==''):
					st.error('Enter the task first')
				elif(len(get_task(new_task)) and task_status==new_task_status and task_to_date==new_task_to_date):
					st.error('Task already exists')
				else:
					edit(new_task,new_task_status,new_task_to_date,task,task_status,task_to_date)
					st.success("Updated Task :: {}".format(task))

					with st.beta_expander("View Updated Data"):
						result = view_data()
						clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
						st.dataframe(clean_df)

	elif choice=='Delete':
		st.subheader("Delete Items")
		data = view_data()
		sf = pd.DataFrame(data,columns=["Task","Status","Due Date"])
		with st.beta_expander("Current data"):
			st.dataframe(sf)

		list_of_tasks = [i[0] for i in view_task()]
		selected_task = st.selectbox("Select Task",list_of_tasks)
		if st.button("Delete"):
			delete(selected_task)
			st.success("Deleted Task: '{}'".format(selected_task))

			with st.beta_expander("Updated Data"):
					result = view_data()
					clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
					st.dataframe(clean_df)


if __name__ == '__main__':
	main()