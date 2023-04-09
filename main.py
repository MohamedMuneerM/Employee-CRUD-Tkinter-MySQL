from db import EmployeeDB
from gui import EmployeeApp



if __name__ == "__main__":
    db = EmployeeDB()
    app = EmployeeApp(db)
    app.mainloop()

