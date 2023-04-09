from mysql.connector import connect, Error
from queries import Query 
import config

class EmployeeDB:
    def __init__(self, conn_data:dict=None):
        conn_data = conn_data or config.DATA
        try:
            self.conn = connect(**conn_data)
            self.cur = self.conn.cursor(dictionary=True)
            self.cur.execute(Query.CREATE_DATABASE)
            self.cur.execute(Query.USE_DATABASE)
            self.cur.execute(Query.CREATE_TABLE)
            self.conn.commit()
            print("Success!")
        except Error as e:
            print(e)

    def get_employee(self, id):
        self.cur.execute(Query.GET_EMPLOYEE, (id,))
        return self.cur.fetchone()
    
    def get_employees(self):
        self.cur.execute(Query.GET_EMPLOYEES)
        return self.cur.fetchall()

    def insert_employee(self, data):
        self.cur.execute(Query.INSERT_EMPLOYEE, list(data.values()))
        self.conn.commit()

    def update_employee(self, id, data):
        employee = self.get_employee(id)
        employee.pop('id')
        employee.update(data)
        data = list(employee.values())
        data.append(id)
        self.cur.execute(Query.UPDATE_EMPLOYEE, data)
        self.conn.commit()

    def delete_employee(self, id):
        self.cur.execute(Query.DELETE_EMPLOYEE, (id,))
        self.conn.commit()

    def show_tables(self):
        self.cur.execute(Query.SHOW_TABLES)
        for db in self.cur:
            print(db) 

    def count(self):
        self.cur.execute(Query.COUNT)
        return self.cur.fetchone()

    def __del__(self):
        self.conn.close()






