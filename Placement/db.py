import mysql.connector


class DB:
    def __init__(self):
        self.connection = mysql.connector.connect(user='root', host='localhost', database='profile')

    def check_user_password(self, email, password):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT email,name FROM student WHERE email='{email}' AND password='{password}' LIMIT 1")
        output = cursor.fetchall()
        cursor.close()

        if not output:
            raise DBException.UserDoesNotExists(f"Incorrect email or password")

    def checck_user_password_coordinator(self, email, password):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM coordinator_login WHERE email='{email}' AND password='{password}' LIMIT 1")
        output = cursor.fetchall()
        cursor.close()
        if not output:
            raise DBException.UserDoesNotExists(f"Incorrect email or password")
        return output[0][0]

    def insert_user(self, data):
        with self.connection.cursor() as cursor:
            self.check_email(data['email'], 'student')
            cursor.execute(f"""
            insert into student (email, name, password)
            values (\'{data['email']}\', \'{data['name']}\',\'{data['password']}\')
            """)
            self.connection.commit()

    def insert_info(self, data):
        with self.connection.cursor() as cursor:
            # self.check_email(data['email'], 'personal_info')
            cursor.execute(
                f"insert into personal_info  (Full_name ,Date_of_birth,Gender,Email, Contact_no) values (\'{data['Fullname']}\', \'{data['DOB']}\',\'{data['gender']}\',\'{data['email']}\',\'{data['phno']}\')")

            cursor.execute(f"""insert into documents (email,10th_marksheet,12th_marksheet,Adhar_No,FE_cgpa,SE_cgpa,TE_cgpa,BE_cgpa) 
            values (\'{data['email']}\',\'{data['10ms']}\',\'{data['12ms']}\',\'{data['aadhar']}\',\'{data['fe']}\',\'{data['se']}\',\'{data['te']}\',\'{data['be']}\')
            """)

            cursor.execute(
                f"""insert into other (email,PRN,ERP,ABCid ,When_you_can_join) values (\'{data['email']}\',\'{data['prn']}\',\'{data['erp']}\',\'{data['abc']}\',\'{data['join']}\')
            """)

            # TODO: FIX THIS
            # cursor.execute(f"""insert into About_you (Email,Github,Linkdin,Portfolic,Skils,Achivements,Extra_Achivements) values (\'{data['email']}\',\'{data['github']}\',\'{data['linkedin']}\',\'{data['skills']}\',\'{data['achievements']}\',\'{data['extraachievements']}\')""")
            self.connection.commit()

    def insert_job_offer(self, companydata):
        email = companydata['email']
        name = companydata['name']
        link = companydata['link']
        required_cgpa = companydata['required_cgpa']
        description = companydata['description']

        with self.connection.cursor() as cursor:
            cursor.execute(f"""insert into coordinator (email, company_name, company_description, registration_link, required_cgpa)
            values ('{email}','{name}', '{description}', '{link}', '{required_cgpa}')""")
        self.connection.commit()

    def get_offers(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""select * from coordinator""")

            offers = []
            for offer in cursor.fetchall():
                offers.append({
                    "name": offer[2],
                    "description": offer[3],
                    "link": offer[4],
                    "required_cgpa": offer[5],
                })

        return offers

    def get_info(self, email):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""select * from personal_info where email='{email}'""")
            print(cursor.fetchall())
            cursor.execute(f"""select * from documents where email='{email}'""")
            print(cursor.fetchall())
            cursor.execute(f"""select * from other where email='{email}'""")
            print(cursor.fetchall())
            cursor.execute(f"""select * from About_you where email='{email}'""")
            print(cursor.fetchall())

    def check_email(self, email, table):
        cursor = self.connection.cursor()
        cursor.execute(f"select email from {table} where email='{email}'")
        email = cursor.fetchall()
        if email:
            raise DBException.UserAlreadyExists(f"{email} already exists")
        cursor.close()


class DBException(Exception):
    class UserAlreadyExists(Exception):
        pass

    class UserDoesNotExists(Exception):
        pass


if __name__ == '__main__':
    db = DB()
    db.get_info('admin@admin.com')
