import mysql.connector


class DB:
    def __init__(self):
        self.connection = mysql.connector.connect(
            user='root', 
            password='Quoltis@0491', 
            host='192.168.0.100', 
            database='profile'
        )

    def check_user_password(self, email, password):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT email, name FROM student WHERE email='{email}' AND password='{password}' LIMIT 1")
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
            self.check_name(data['name'], 'student')
            cursor.execute(f"""
            insert into student (email, name, password)
            values (\'{data['email']}\', \'{data['name']}\',\'{data['password']}\')
            """)
            self.connection.commit()

    def insert_info(self, data):
        with self.connection.cursor() as cursor:
            # self.check_email(data['email'], 'personal_info')
            cursor.execute(
                f"insert into personal_info (Full_name ,Date_of_birth,Gender,Email, Contact_no) values (\'{data['Fullname']}\', \'{data['DOB']}\',\'{data['gender']}\',\'{data['email']}\',\'{data['phno']}\')")

            cursor.execute(f"""insert into documents (email,10th_marksheet,12th_marksheet,Adhar_No,FE_cgpa,SE_cgpa,TE_cgpa,BE_cgpa) 
            values (\'{data['email']}\',\'{data['10ms']}\',\'{data['12ms']}\',\'{data['aadhar']}\',\'{data['fe']}\',\'{data['se']}\',\'{data['te']}\',\'{data['be']}\')
            """)

            cursor.execute(
                f"""insert into other (email,PRN,ERP,ABCid ,When_you_can_join) values (\'{data['email']}\',\'{data['prn']}\',\'{data['erp']}\',\'{data['abc']}\',\'{data['join']}\')
            """)

            cursor.execute(f"""insert into about_you (Email,Github,Linkdin,Portfolic,Skils,Achivements,Extra_Achivements) values (\'{data['email']}\',\'{data['github']}\',\'{data['linkedin']}\',\'{data['pweb']}\',\'{data['skills']}\',\'{data['achievements']}\',\'{data['extraachievements']}\');""")
            self.connection.commit()

    def insert_job_offer(self, companydata):
        email = companydata['email']
        name = companydata['name']
        role = companydata['role']
        description = companydata['description']
        stud_branch = companydata['stud_branch']
        link = companydata['link']
        due_date = companydata['due_date']

        with self.connection.cursor() as cursor:
            cursor.execute("""insert into coordinator (email, name, role, description, branch, link, due_date) 
            values ('{email}', '{name}', '{role}', '{description}', '{branch}', '{link}', '{due_date}')""".format(
                email=email,
                name=name,
                role=role,
                description=description,
                branch=stud_branch,
                link=link,
                due_date=due_date
            ))
        self.connection.commit()

    def get_offers(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from coordinator")

            offers = []
            for offer in cursor.fetchall():
                offers.append({
                    "id": offer[0],
                    "email": offer[1],
                    'name': offer[2],
                    "role": offer[3],
                    "description": offer[4],
                    "branch": offer[5],
                    "location": offer[6],
                    "link": offer[7],
                    "due_date": offer[8]
                })

        return offers

    def get_info(self, email):
        with self.connection.cursor() as cursor:
            data = {}
            cursor.execute(f"""select * from personal_info where Email='{email}' LIMIT 1;""")
            output = cursor.fetchall()
            if not output:
                return None
            data['Fullname'] = output[0][1]
            data['DOB'] = output[0][2]
            data['gender'] = output[0][3]
            data['email'] = email
            data['phno'] = output[0][5]
            cursor.execute(f"""select * from documents where email='{email}' LIMIT 1;""")
            output = cursor.fetchall()
            data['10ms'] = output[0][2]
            data['12ms'] = output[0][3]
            data['aadhar'] = output[0][4]
            data['fe'] = output[0][5]
            data['se'] = output[0][6]
            data['te'] = output[0][7]
            data['be'] = output[0][8]
            cursor.execute(f"""select * from other where Email='{email}' LIMIT 1;""")
            output = cursor.fetchall()
            data['prn'] = output[0][2]
            data['erp'] = output[0][3]
            data['abc'] = output[0][4]
            data['join'] = output[0][5]
            cursor.execute(f"""select * from About_you where Email='{email}' LIMIT 1;""")
            output = cursor.fetchall()
            data['github'] = output[0][2]
            data['linkedin'] = output[0][3]
            data['pweb'] = output[0][4]
            data['skills'] = output[0][5]
            data['achievements'] = output[0][6]
            data['extraachievements'] = output[0][7]

        return data

    def check_email(self, email, table):
        cursor = self.connection.cursor()
        cursor.execute(f"select email from {table} where email='{email}'")
        email = cursor.fetchall()
        if email:
            raise DBException.UserAlreadyExists(f"{email} already exists")
        cursor.close()

    def check_name(self, name, table):
        cursor = self.connection.cursor()
        cursor.execute(f"select name from {table} where name='{name}'")
        name = cursor.fetchall()
        if name:
            raise DBException.UserAlreadyExists(f"{name} already exists")
        cursor.close()

    def delete_job_offer(self, jobId):
        with self.connection.cursor() as cursor:
            cursor.execute("delete from coordinator where id='{jobId}'".format(jobId=jobId))

        self.connection.commit()


class DBException(Exception):
    class UserAlreadyExists(Exception):
        pass

    class UserDoesNotExists(Exception):
        pass
