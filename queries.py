class Query:
        CREATE_DATABASE = """ CREATE DATABASE IF NOT EXISTS EMPLOYEECRUD """
        CREATE_TABLE = """
            CREATE TABLE IF NOT EXISTS employee (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(240) NOT NULL,
            enroll_number INT(6) NOT NULL,
            age SMALLINT NOT NULL,
            profile_picture LONGBLOB,
            profile_pic_name TEXT,
            dob DATE NOT NULL,
            joined_date DATE NOT NULL,
            basic_salary DECIMAL(10, 2) NOT NULL,
            lpa DECIMAL(12, 2) NOT NULL
            );"""
        USE_DATABASE = """ USE EMPLOYEECRUD """
        SHOW_TABLES = """ SHOW TABLES """
        GET_EMPLOYEE = """ SELECT * FROM employee WHERE id = %s """
        GET_EMPLOYEES = """ SELECT * FROM employee """

        INSERT_EMPLOYEE = """ 
                            INSERT INTO employee (name, enroll_number, age, profile_picture, profile_pic_name, dob, joined_date, basic_salary, lpa)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        UPDATE_EMPLOYEE = """ UPDATE employee SET name = %s, enroll_number = %s, age = %s, profile_picture = %s, profile_pic_name = %s, dob = %s, joined_date = %s, basic_salary = %s, lpa = %s  WHERE id = %s """
        DELETE_EMPLOYEE = """ DELETE FROM employee WHERE id=%s """
        COUNT = """ SELECT COUNT(*) as total_employees from employee """

