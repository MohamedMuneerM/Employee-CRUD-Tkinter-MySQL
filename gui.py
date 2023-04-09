import tkinter as tk
import base64
from io import BytesIO
from datetime import date, datetime
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from tkcalendar import DateEntry
from PIL import Image, ImageTk



class FormFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.name_var = tk.StringVar()
        self.enroll_number_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.dob_var = tk.StringVar()
        self.joined_date_var = tk.StringVar()
        self.basic_salary_var = tk.StringVar()
        self.lpa_var = tk.StringVar()
        self.profile_picture_var = tk.StringVar()

        self.grid(row=1, column=0, padx=10, pady=10)

        tk.Label(self, text="Name:").grid(row=0, column=0)
        tk.Entry(self, textvariable=self.name_var, width=35).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Enroll Number:").grid(row=0, column=2)
        tk.Spinbox(self, textvariable=self.enroll_number_var, from_=1, to=999999, increment=1, width=15).grid(row=0, column=3, padx=10, pady=10)
        
        tk.Label(self, text="DOB:").grid(row=0, column=4, padx=10, pady=10)
        DateEntry(self, textvariable=self.dob_var, date_pattern='dd/MM/yyyy', width=12, state='readonly').grid(row=0, column=5, padx=10, pady=10) 
        
        tk.Label(self, text="Profile Picture:").grid(row=1, column=0)
        tk.Entry(self, textvariable=self.profile_picture_var, state="readonly").grid(row=1, column=1)
        tk.Button(self, text="Browse", command=self.browse_profile_picture).grid(row=2, column=1, padx=(10,0))
        
        tk.Label(self, text="Joined Date:").grid(row=1, column=2, padx=10, pady=10)
        DateEntry(self, textvariable=self.joined_date_var, date_pattern='dd/MM/yyyy', width=12, state='readonly').grid(row=1, column=3, padx=10, pady=10) 
        
        tk.Label(self, text="Basic Salary:").grid(row=1, column=4)
        tk.Spinbox(self, textvariable=self.basic_salary_var, from_=0, to=100, increment=1, width=10).grid(row=1, column=5, padx=10, pady=10)
        
        tk.Label(self, text="LPA:").grid(row=1, column=6, padx=10, pady=10)
        tk.Label(self, textvariable=self.lpa_var).grid(row=1, column=7, padx=10, pady=10)

        
        tk.Button(self, text="Add", command=self.parent.add_employee, width=15).grid(row=3, column=1, columnspan=1, padx=10, pady=10, sticky='ew')
        tk.Button(self, text="Update", command=self.parent.update_employee).grid(row=3, column=2, padx=10, pady=10, sticky='ew')
        tk.Button(self, text="Delete", command=self.parent.delete_employee).grid(row=3, column=3,columnspan=1, padx=10, pady=10, sticky='ew')
        tk.Button(self, text="Clear", command=self.parent.clear_fields).grid(row=3, column=4, columnspan=1, padx=10, pady=10, sticky='ew')

        
    def browse_profile_picture(self):
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.gif"),))
        self.profile_picture_var.set(file_path)



class TableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid(row=2, column=0, padx=10, pady=10)
        self.table = ttk.Treeview(self)
        self.table.grid(row=0, column=0, columnspan=3)
        
        self.table['columns'] = ('No.', 'Name', 'Enroll Number', 'Age', 'photo_pic_name', 'Date Of Birth', 'Joined Date', 'Basic Salary', 'LPA')

        self.table.column("#0", width=0,  stretch='NO')
        self.table.column("No.",anchor='center', width=40)
        self.table.column("Name",anchor='center',width=200)
        self.table.column("Enroll Number",anchor='center',width=90)
        self.table.column("Age",anchor='center',width=40)
        self.table.column("photo_pic_name", width=0, stretch='NO')
        self.table.column("Date Of Birth",anchor='center',width=90)
        self.table.column("Joined Date",anchor='center',width=90)
        self.table.column("Basic Salary",anchor='center',width=90)
        self.table.column("LPA",anchor='center',width=140)

        self.table.heading("#0", text="", anchor='center')
        self.table.heading("No.",anchor='center', text='No.')
        self.table.heading("Name",anchor='center',text='Employee Name')
        self.table.heading("Enroll Number",anchor='center',text='Enroll Number')
        self.table.heading("Age",anchor='center',text='Age')
        self.table.heading("Date Of Birth",anchor='center',text='Date Of Birth')
        self.table.heading("Joined Date", anchor='center',text='Joined Date')
        self.table.heading("Basic Salary",anchor='center',text='Basic Salary')
        self.table.heading("LPA",anchor='center',text='Lakhs Per Annum(LPA)')

        self.table.bind('<<TreeviewSelect>>', self.parent.populate_fields) # bind listbox selection event to populate_fields method
        self.table.bind('<Double-1>', self.parent.profile_view)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row=0, column=3, sticky='ns')
        self.table.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.table.yview)



class TitleFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.total_employees_var = tk.StringVar()
        self.total_employees_var.set("0")
        self.grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self, text="Employee Management System", font=("Helvetica", 20)).grid(row=0, column=0)
        tk.Label(self, text=f"Total employees: " , font=("Helvetica", 10)).grid(row=0, column=3)
        tk.Label(self, textvariable=self.total_employees_var, font=("Helvetica", 10)).grid(row=0, column=4)



class EmployeeApp(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.title("Employee CRUD")
        self.geometry("900x600")
        self.resizable(False, False)
        self.db = db
        self.title_frame = TitleFrame(self)
        self.title_frame.total_employees_var.set(self.get_current_employees_count())
        self.form_frame = FormFrame(self)
        self.table_frame = TableFrame(self)
        self.populate_table()

    def get_current_employees_count(self):
        return str(self.db.count()['total_employees'])

    def convert_image(self, profile_picture):
        image = Image.open(str(profile_picture))
        profile_pic_name = image.filename

        width = 155
        height = int((float(image.size[1]) / float(image.size[0])) * width)
        image = image.resize((width, height), Image.ANTIALIAS)

        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        return profile_pic_name, base64.b64encode(buffer.getvalue())
    
    
    def profile_view(self, _):
        selected_employee_id = int(self.table_frame.table.selection()[0])
        data = self.db.get_employee(selected_employee_id)
        profile_window = tk.Toplevel(self)
        profile_window.title("Employee Profile")
        profile_window.geometry("600x600")

        image_data = data['profile_picture']

        if image_data is not None:
            image_data = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_data))
        else:
            _, image_data = self.convert_image('profile_image.jpg')
            image_data = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_data))

        image = ImageTk.PhotoImage(image)
        photo = tk.Label(profile_window, image=image)
        photo.img = image
        photo.pack()
        tk.Label(profile_window, text="Employee Details", font=("Helvetica", 18)).pack(pady=10)
        tk.Label(profile_window, text="Name: {}".format(data['name']), font=("Helvetica", 14)).pack()
        tk.Label(profile_window, text="Enroll Number: {}".format(data['enroll_number']),
                 font=("Helvetica", 14)).pack()
        tk.Label(profile_window, text="Age: {}".format(data['age']),font=("Helvetica", 14)).pack()
        tk.Label(profile_window, text="Date of Birth: {}".format(data['dob']),
                 font=("Helvetica", 14)).pack()
        tk.Label(profile_window, text="Joined Date: {}".format(data['joined_date']),
                 font=("Helvetica", 14)).pack()
        tk.Label(profile_window, text="Basic Salary: {}".format(data['basic_salary']),
                 font=("Helvetica", 14)).pack()
        tk.Label(profile_window, text="LPA: {}".format(data['lpa']), font=("Helvetica", 14)).pack()

        profile_picture_label = tk.Label(profile_window)
        profile_picture_label.pack()

    def clear_all(self):
        for item in self.table_frame.table.get_children():
            self.table_frame.table.delete(item)

    def clear_fields(self):
        self.form_frame.name_var.set('')
        self.form_frame.enroll_number_var.set('')
        self.form_frame.age_var.set('')
        self.form_frame.profile_picture_var.set('')
        self.form_frame.dob_var.set('')
        self.form_frame.joined_date_var.set('')
        self.form_frame.basic_salary_var.set('')
        self.form_frame.lpa_var.set('')


    def calculate_age(self, d):
        today = date.today()
        day, month, year = d.split('/')
        d = date(day=int(day), month=int(month), year=int(year))
        return today.year - d.year - ((today.month, today.day) < (d.month, d.day))
    
    def validate(self, name, enroll_number, joined_date, basic_salary):
        if len(name) > 15 or len(name) < 3:
            messagebox.showerror("Name Length Error", "Name must above 3 characters and below 15 character")
            return False
        elif not enroll_number.isdigit():
            messagebox.showerror("Invalid Enroll Number", "Invalid Enroll Number")
            return False
        elif len(str(enroll_number)) < 6:
            messagebox.showerror("Enroll Number Length Error", "Enroll Number must not be below 6 digits") 
            return False       
        elif self.calculate_age(joined_date) < 18:
            messagebox.showerror("Joined Date", "Joined Date must be not less than 18 years")
            return False
        elif not basic_salary.isdigit():
            messagebox.showerror("Invalid Salary", "Invalid Salary Number")
            return False
        elif float(basic_salary) < 10000:
            messagebox.showerror("Basic Salary", "Salary must be not less than 10000 rupees")
            return False
        elif float(basic_salary) > 9999999:
            messagebox.showerror("Higher salary", "Salary cannot be more than 9999999 rupees")
            return False
        
        return True
    
    
    def populate_table(self):
        self.clear_all()
        items = self.db.get_employees()

        for index, item in enumerate(items, 1):
            id = item.pop('id')
            item.pop('profile_picture')

            item = list(item.values())
            item.insert(0, index)
            self.table_frame.table.insert(parent='',index='end', iid=id, text='', values=item)


    def populate_fields(self, _):
        if self.table_frame.table.selection():
            selected_employee = self.table_frame.table.item(self.table_frame.table.selection()[0])['values']

            dob = datetime.strptime(selected_employee[5], "%Y-%m-%d")
            dob = dob.strftime("%d/%m/%Y")

            joined_date = datetime.strptime(selected_employee[6], "%Y-%m-%d")
            joined_date = joined_date.strftime("%d/%m/%Y")

            self.form_frame.name_var.set(selected_employee[1])
            self.form_frame.enroll_number_var.set(selected_employee[2])
            self.form_frame.age_var.set(selected_employee[3])
            self.form_frame.profile_picture_var.set(selected_employee[4])
            self.form_frame.dob_var.set(dob)
            self.form_frame.joined_date_var.set(joined_date)
            self.form_frame.basic_salary_var.set(int(float(selected_employee[7])))
            self.form_frame.lpa_var.set(selected_employee[8])

    def add_employee(self):

        name = self.form_frame.name_var.get()
        enroll_number = self.form_frame.enroll_number_var.get()
        dob = self.form_frame.dob_var.get()
        joined_date = self.form_frame.joined_date_var.get()
        basic_salary = self.form_frame.basic_salary_var.get()
        profile_picture = self.form_frame.profile_picture_var.get() or None

        if self.validate(name, enroll_number, joined_date, basic_salary):

            base64_string = None
            profile_pic_name = None
            if profile_picture is not None and profile_picture != 'None':
                profile_pic_name, base64_string = self.convert_image(profile_picture)

            data =  {
                "name" : name,
                "enroll_number": enroll_number,
                "age": self.calculate_age(dob),
                "profile_picture": base64_string,
                "profile_pic_name": profile_pic_name,
                "dob": datetime.strptime(dob, '%d/%m/%Y'),
                "joined_date": datetime.strptime(joined_date, '%d/%m/%Y'),
                "basic_salary": basic_salary,
                "lpa": float(basic_salary) * 12
            }

            self.db.insert_employee(data=data)

            self.populate_table()
            total_employees = self.get_current_employees_count()
            self.title_frame.total_employees_var.set(total_employees)

    def delete_employee(self):

        selected_index = self.table_frame.table.selection()
        if not selected_index:
            messagebox.showerror("Error", "No employee selected!")
            return
        
        selected_items = self.table_frame.table.selection()
        areyousure = messagebox.askquestion('Are you Sure ', 'Do you want to delete the selected item(s)?',
                                        icon='warning')
        if areyousure == 'yes':
            for index in selected_items:
                self.db.delete_employee(int(index))
                self.table_frame.table.delete(index)

            self.populate_table()
            self.clear_fields()
            total_employees = self.get_current_employees_count()
            self.title_frame.total_employees_var.set(total_employees)


    def update_employee(self):

        selected_index = self.table_frame.table.selection()
        if not selected_index:
            messagebox.showerror("Error", "No employee selected!")
            return

        areyousure = messagebox.askquestion('Are you Sure ', 'Do you want to update the selected item?',
                                        icon='warning')
        
        if areyousure == 'yes':
            id = int(self.table_frame.table.selection()[0])
            name = self.form_frame.name_var.get()
            enroll_number = self.form_frame.enroll_number_var.get()
            dob = self.form_frame.dob_var.get()
            joined_date = self.form_frame.joined_date_var.get()
            basic_salary = self.form_frame.basic_salary_var.get()
            profile_picture = self.form_frame.profile_picture_var.get() or None
            if self.validate(name, enroll_number, joined_date, basic_salary):
                base64_string = None
                profile_pic_name = None
                if profile_picture != 'None':
                    profile_pic_name, base64_string = self.convert_image(profile_picture)


                data =  {
                    "name" : name,
                    "enroll_number": enroll_number,
                    "age": self.calculate_age(dob),
                    "profile_picture": base64_string,
                    "profile_pic_name": profile_pic_name,
                    "dob": datetime.strptime(dob, '%d/%m/%Y'),
                    "joined_date": datetime.strptime(joined_date, '%d/%m/%Y'),
                    "basic_salary": basic_salary,
                    "lpa": float(basic_salary) * 12
                }

                self.db.update_employee(id, data)
                self.populate_table()
                self.clear_fields()
                total_employees = self.get_current_employees_count()
                self.title_frame.total_employees_var.set(total_employees)


