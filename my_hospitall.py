import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='hospital_bhai'
        )
        if mydb.is_connected():
            print("Connected to MySQL database")
        return mydb
    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(mydb):
    if mydb.is_connected():
        mydb.close()
        print("MySQL connection is closed")
    
# Function to ensure at least one hospital exists in the table
def ensure_default_hospital(hospital_id, name, address, phone, email):
    mydb = create_connection()
    if mydb is None:
        return

    cursor = mydb.cursor()
    try:
        # Insert hospital credentials into hospital table
        hospital_insert_query = """
        INSERT INTO hospital (hospital_id, name, address, phone, email)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(hospital_insert_query, (hospital_id, name, address, phone, email))
        mydb.commit()
        print("Default hospital created.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        close_connection(mydb)

# Function to get a valid hospital ID from the user
def get_hospital_id(cur):
    cur.execute("SELECT hospital_id, name FROM hospital")
    hospitals = cur.fetchall()
    if not hospitals:
        print("No hospitals found. Please add a hospital first.")
        return None
    print("Available Hospitals:")
    for hospital in hospitals:
        print(f"ID: {hospital[0]}, Name: {hospital[1]}")
    return int(input("Enter the hospital ID: "))

def get_hospital():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM hospital")
    hospitals = cursor.fetchall()
    if not hospitals:
        print("No hospitals found. Please add a hospital first.")
        return None
    print("Available Hospitals:")
    for hospital in hospitals:
        
        print(f"ID:{hospital[0]} , Name:{hospital[1]} , address:{hospital[2]} , phone:{hospital[3]} , email:{hospital[4]}")
    cursor.close() 
    close_connection(connection)


# User Registration (Patients and Doctors)
def signup_user(username, password, user_type):
    mydb = create_connection()
    if mydb is None:
        return
    
    cur = mydb.cursor()
    # Get a valid hospital ID
    hospital_id = get_hospital_id(cur)

    # Insert user credentials into users table
    user_insert_query = """
    INSERT INTO users (username, password, user_type, hospital_id)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(user_insert_query, (username, password, user_type, hospital_id))
    mydb.commit()
    
    print("your username,password are created sussefully")
    # Get the user_id of the newly created user
    user_id = cur.lastrowid

    if user_type == 'patient':
        print("fill patients details")
        # Insert patient details
        patient_insert_query = """
        INSERT INTO patients (user_id, hospital_id, name, address, phone, date_of_birth, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        name = input("Enter your name: ")
        address = input("Enter your address: ")
        phone = input("Enter your phone number: ")
        date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ")
        email = input("Enter your email: ")
        cur.execute(patient_insert_query, (user_id, hospital_id, name, address, phone, date_of_birth, email))
    
    elif user_type == 'doctor':
        print("Fill doctor details :")
        # Insert doctor details
        doctor_insert_query = """
        INSERT INTO doctors (user_id, hospital_id, name, specialization, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        name = input("Enter your name: ")
        specialization = input("Enter your specialization: ")
        phone = input("Enter your phone number: ")
        email = input("Enter your email: ")
        cur.execute(doctor_insert_query, (user_id, hospital_id, name, specialization, phone, email))

    mydb.commit()
    cur.close()
    close_connection(mydb)
    print("Signup successful!")

# Fill Personal Details for user_type
def Fill_details(user_type,user_id):
    mydb = create_connection()
    if mydb is None:
        return
    
    cur = mydb.cursor()
    # Get a valid hospital ID
    hospital_id = get_hospital_id(cur)
    
    if user_type == 'patient':
        print("fill patients details")
        # Insert patient details
        patient_insert_query = """
        INSERT INTO patients (user_id, hospital_id, name, address, phone, date_of_birth, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        name = input("Enter your name: ")
        address = input("Enter your address: ")
        phone = input("Enter your phone number: ")
        date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ")
        email = input("Enter your email: ")
        cur.execute(patient_insert_query, (user_id, hospital_id, name, address, phone, date_of_birth, email))
    
    elif user_type == 'doctor':
        print("Fill doctor details :")
        # Insert doctor details
        doctor_insert_query = """
        INSERT INTO doctors (user_id, hospital_id, name, specialization, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        D="Dr."
        n= input("Enter your name: ")
        name = D + n
        specialization = input("Enter your specialization: ")
        phone = input("Enter your phone number: ")
        email = input("Enter your email: ")
        cur.execute(doctor_insert_query, (user_id, hospital_id, name, specialization, phone, email))

    mydb.commit()
    cur.close()
    close_connection(mydb)
    print("Fill Your Details successful!")


# Login and Authentication
def login_user(username, password):
    connection = create_connection()
    if connection is None:
        return None

    cursor = connection.cursor()

    login_query = """
    SELECT user_id, user_type FROM users
    WHERE username = %s AND password = %s
    """
    cursor.execute(login_query, (username, password))
    user = cursor.fetchone()
    
    cursor.close()
    close_connection(connection)

    if user:
        print("Login successful!")
        return user
    else:
        print("Invalid username or password.")
        return None
    
#display_token
def display_token(patient_id):
    try:
        # Establish the database connection
        connection = create_connection()
        cursor = connection.cursor()
        
        # Define the query to fetch tokens for the given patient_id
        display_query = """
            SELECT * FROM tokens WHERE patient_id = %s
        """        
        # Execute the query with the patient_id parameter
        cursor.execute(display_query, (patient_id,))
        
        # Fetch all results
        tokens = cursor.fetchall()
        
        # Retrieve column names
        column_names=['token_id', 'patient_id', 'doctor_id', 'hospital_id', 'issue_date', 'status', 'visit_time']

        # Check if any tokens were found
        if tokens:
            for token in tokens:
                #print(token,type(token))
                # Create a dictionary of column names and their corresponding values
                token_dict = dict(zip(column_names, token))
                #print(token_dict)
                #                 
                # Print key-value pairs
                for key, value in token_dict.items():
                    print(f"{key}: {value}")
                print("-" * 30)
        else:
            print("No tokens found for this patient ID.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the cursor and connection are closed properly
        if cursor:
            cursor.close()
        if connection:
            close_connection(connection)

# Token Management
def issue_token(patient_id, doctor_id):
    connection = create_connection()
    cursor = connection.cursor()

    token_insert_query = """
    INSERT INTO tokens (patient_id, doctor_id, hospital_id, issue_date)
    VALUES (%s, %s, (SELECT hospital_id FROM patients WHERE patient_id = %s), NOW())
    """
    cursor.execute(token_insert_query, (patient_id, doctor_id,patient_id))
    connection.commit()

    cursor.close()
    close_connection(connection)
    print("Token issued successfully!")

#using by doctor update payment status
def update_token_status(token_id, status):
    connection = create_connection()
    cursor = connection.cursor()

    token_update_query = """
    UPDATE tokens SET status = %s, visit_time = NOW() WHERE token_id = %s
    """
    cursor.execute(token_update_query, (status, token_id))
    connection.commit()
    cursor.close() 
    close_connection(connection)
    print("Token status updated successfully!")

# Appointment Booking
def book_appointment(patient_id, doctor_id,hospital_id, appointment_date):
    connection = create_connection()
    cursor = connection.cursor()

    appointment_insert_query = """
    INSERT INTO appointments (patient_id, doctor_id,hospital_id, appointment_date)
    VALUES (%s, %s, %s,%s)
    """
    cursor.execute(appointment_insert_query, (patient_id, doctor_id,hospital_id, appointment_date))
    connection.commit()

    issue_token(patient_id, doctor_id)  # Issue a token for the appointment

    cursor.close()
    close_connection(connection)
    print("Appointment booked successfully!")

#search_specialization
def search_specialization():
    connection = create_connection()
    cursor = connection.cursor()
    s_specialization=""" select distinct specialization from doctors"""
    cursor.execute(s_specialization)
    s = cursor.fetchall()

    if s:
        print("specialization List:")
        a=1
        global dict_specialization
        dict_specialization={}
        for ss in s:
            dict_specialization.setdefault(a,ss[0])
            print(a," : ",ss[0])
            a=a+1
        #print(dict_specialization)   
    else:
        print("not found specialization!!!!!")
    cursor.close()
    close_connection(connection)

#display_doctor_specialization
def display_doctor_specialization(choice):
    connection = create_connection()
    cursor = connection.cursor()
    global dict_specialization
    ch=dict_specialization[choice]
    chh=(ch,)
    base_query = """
    SELECT doctor_id, name, specialization, phone, email
    FROM doctors  WHERE specialization = %s
    """
    cursor.execute(base_query,chh)
    doctors = cursor.fetchall()

    if doctors:
        print("Doctor List:")
        for doctor in doctors:
            doctor_id, name, specialization, phone, email = doctor
            print(f"Doctor ID: {doctor_id}")
            print(f"Name: {name}")
            print(f"Specialization: {specialization}")
            print(f"Phone: {phone}")
            print(f"Email: {email}")
            print("-" * 30)
    else:
        print("No doctors found matching the criteria.")
    cursor.close()
    close_connection(connection)

# Billing and Payments
def pay_bill(patient_id,hospital_id,amount):
    connection = create_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO billing (patient_id, hospital_id, amount, payment_status,billing_date)
        VALUES (%s, %s, %s, 'paid',NOW())
        """
        
    # Execute the SQL query with the provided parameters
    cursor.execute(insert_query, (patient_id, hospital_id, amount))
        
    # Commit the transaction to save changes
    connection.commit()
    cursor.close()
    close_connection(connection)
    print("Bill paid successfully!")

# Doctors Display
def display_doctor_list(filter_type=None, filter_value=None):
    connection = create_connection()
    cursor = connection.cursor()

    base_query = """
    SELECT doctor_id, name, specialization, phone, email
    FROM doctors
    """

    if filter_type == 'specialization':
        query = base_query + " WHERE specialization = %s"
        params = (filter_value,)
    elif filter_type == 'name':
        query = base_query + " WHERE name LIKE %s"
        params = ('%' + filter_value + '%',)
    else:
        query = base_query
        params = ()

    cursor.execute(query, params)
    doctors = cursor.fetchall()

    if doctors:
        print("Doctor List:")
        for doctor in doctors:
            doctor_id, name, specialization, phone, email = doctor
            print(f"Doctor ID: {doctor_id}")
            print(f"Name: {name}")
            print(f"Specialization: {specialization}")
            print(f"Phone: {phone}")
            print(f"Email: {email}")
            print("-" * 30)
    else:
        print("No doctors found matching the criteria.")
    cursor.close()
    close_connection(connection)
#display doctor profile
def doctor_profile(doctor_id):
    try:
        # Create a database connection
        connection = create_connection()
        cursor = connection.cursor()

        # Define the query to fetch doctor details
        base_query = """
        SELECT doctor_id,user_id,hospital_id, name, specialization, phone, email
        FROM doctors
        WHERE doctor_id = %s
        """
        # Execute the query
        cursor.execute(base_query, (doctor_id,))
        # Fetch the result
        doc = cursor.fetchone()

        # Check if a record was found
        if doc:
            print("\nDoctor Profile")
            print(f"ID: {doc[0]}")
            print(f"Use ID: {doc[1]}")
            print(f"Hostipal ID: {doc[2]}")
            print(f"Name: {doc[3]}")
            print(f"Specialization: {doc[4]}")
            print(f"Phone: {doc[5]}")
            print(f"Email: {doc[6]}")
        else:
            print("No doctor found with the given ID.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Ensure resources are released
        if connection:
            cursor.close()
            connection.close()
#view doctor user details
def view_user_dp(username):
    connection = create_connection()
    cursor = connection.cursor()
    base_query=""" select * from users where username=%s
               """
    cursor.execute(base_query,(username,))
    user=cursor.fetchone()
    if user:
        print("\n your user details:")
        print(f"User ID: {user[0]}")
        print(f"Hospital ID: {user[1]}")
        print(f"Username: {user[2]}")
        print(f"Password: {user[3]}")
        print(f"User Type: {user[4]}")
    else:
        print("not found user")
    cursor.close()
    connection.close()
# View All Appointments
def view_appointments(doctor_id):
    connection = create_connection()
    cursor = connection.cursor()

    appointment_query = """
    SELECT a.appointment_id, p.name, a.appointment_date FROM appointments a JOIN patients p 
    ON a.patient_id = p.patient_id WHERE a.doctor_id = %s
    """
    cursor.execute(appointment_query, (doctor_id,))
    appointments = cursor.fetchall()

    if appointments:
        print("\nYour Appointments:")
        for appointment in appointments:
            print(f"Appointment ID: {appointment[0]}")
            print(f"Patient Name: {appointment[1]}")
            print(f"Appointment Date: {appointment[2]}")
            print("-" * 30)
    else:
        print("No appointments found.")
    cursor.close()
    close_connection(connection)

# View All Users
def view_all_users():
    connection = create_connection()
    cursor = connection.cursor()

    user_query = """
    SELECT user_id, username, user_type FROM users
    """
    cursor.execute(user_query)
    users = cursor.fetchall()

    if users:
        print("\nAll Users:")
        for user in users:
            print(f"User ID: {user[0]}")
            print(f"Username: {user[1]}")
            print(f"User Type: {user[2]}")
            print("-" * 30)
    else:
        print("No users found.")
    cursor.close()
    close_connection(connection)

#view all patient
def all_patient():
    connection = create_connection()
    cursor = connection.cursor()

    user_query = """
    SELECT * FROM patients
    """
    cursor.execute(user_query)
    users = cursor.fetchall()

    if users:
        print("\nAll Users:")
        for user in users:
            print(f"Patient ID: {user[0]}")
            print(f"User ID: {user[1]}")
            print(f"Hospital ID: {user[2]}")
            print(f"Name: {user[3]}")
            print(f"Address: {user[4]}")
            print(f"Phone: {user[5]}")
            print(f"Date of birth: {user[6]}")
            print(f"Email Id: {user[7]}")
            print("-" * 30)
    else:
        print("No users found.")
    cursor.close()
    close_connection(connection)
# view patient by id
def view_patient(patient_id):
    connection = create_connection()
    cursor = connection.cursor()

    user_query = """
    SELECT * FROM patients where patient_id=%s
    """
    cursor.execute(user_query,(patient_id,))
    user = cursor.fetchone()

    if user:
        print("\nUser details:")
        print(f"Patient ID: {user[0]}")
        print(f"User ID: {user[1]}")
        print(f"Hospital ID: {user[2]}")
        print(f"Name: {user[3]}")
        print(f"Address: {user[4]}")
        print(f"Phone: {user[5]}")
        print(f"Date of birth: {user[6]}")
        print(f"Email Id: {user[7]}")
        print("-" * 30)
    else:
        print("No users found.")
    cursor.close()
    close_connection(connection)

# View All Appointments
def view_all_appointments():
    connection = create_connection()
    cursor = connection.cursor()

    appointment_query = """
    SELECT a.appointment_id, p.name AS patient_name, d.name AS doctor_name, a.appointment_date
    FROM appointments a
    JOIN patients p ON a.patient_id = p.patient_id
    JOIN doctors d ON a.doctor_id = d.doctor_id
    """
    cursor.execute(appointment_query)
    appointments = cursor.fetchall()

    if appointments:
        print("\nAll Appointments:")
        for appointment in appointments:
            print(f"Appointment ID: {appointment[0]}")
            print(f"Patient Name: {appointment[1]}")
            print(f"Doctor Name: {appointment[2]}")
            print(f"Appointment Date: {appointment[3]}")
            print("-" * 30)
    else:
        print("No appointments found.")
    cursor.close()
    close_connection(connection)

# Display Patient Bill
def display_patient_bill(patient_id):
    connection = create_connection()
    cursor = connection.cursor()

    billing_query = """
    SELECT bill_id, amount, payment_status, billing_date
    FROM billing
    WHERE patient_id = %s
    """
    cursor.execute(billing_query, (patient_id,))
    bills = cursor.fetchall()

    if bills:
        print(f"Billing details for patient ID {patient_id}:")
        for bill in bills:
            bill_id, amount, payment_status, billing_date = bill
            print(f"Bill ID: {bill_id}")
            print(f"Amount: {amount:.2f}")
            print(f"Payment Status: {payment_status}")
            print(f"Billing Date: {billing_date}")
            print("-" * 30)
    else:
        print("No billing records found for this patient.")
    cursor.close()
    close_connection(connection)

def admin_user(username, password):
    # Define admin credentials
    admin_email = "admin@gmail.com"
    admin_password = '12345'

    # Check if provided credentials match the admin credentials
    if username == admin_email and password == admin_password:
        while True:
            print("\nAdmin Menu")
            print("1. View All Users")
            print("2. View All Appointments")
            print("3. Display Patient Bill")
            print("4. Display Doctors")
            print("5. View All patient")
            print("6. Logout")

            try:
                # Get user choice and handle menu options
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    view_all_users()
                elif choice == 2:
                    view_all_appointments()
                elif choice == 3:
                    patient_id = int(input("Enter patient ID: "))
                    display_patient_bill(patient_id)
                elif choice == 4:
                    while True:
                        print("\nDoctor List Options:")
                        print("1. Display All Doctors")
                        print("2. Display Doctors by Specialization")
                        print("3. Display Doctors by Name")
                        print("4. Exit")

                        try:
                            list_choice = int(input("Enter your choice (1-4): ").strip())
                            
                            if list_choice == 1:
                                display_doctor_list()
                            
                            elif list_choice == 2:
                                search_specialization()
                                try:
                                    specialization_choice = int(input("Enter your specialization choice: ").strip())
                                    display_doctor_specialization(specialization_choice)
                                except ValueError:
                                    print("Invalid input. Please enter a valid number for specialization.")
                            
                            elif list_choice == 3:
                                name_filter = input("Enter name or partial name: ").strip()
                                display_doctor_list('name', name_filter)
                            
                            elif list_choice == 4:
                                print("Exiting...")
                                break
                            
                            else:
                                print("Invalid choice. Please enter a number between 1 and 4.")
                        
                        except ValueError:
                            print("Invalid input. Please enter a number between 1 and 4.")
                        except Exception as e:
                            print(f"An error occurred: {e}")

                elif choice ==5:
                    while True:
                        print("\nMenu")
                        print("1. View All Patients")
                        print("2. View Patient by ID")
                        print("3. Exit")
                        try:
                            choice = int(input("Enter your choice: "))

                            if choice == 1:
                                all_patient()
                            elif choice == 2:
                                try:
                                    patient_id = int(input("Enter the patient ID: "))
                                    view_patient(patient_id)
                                except ValueError:
                                    print("Invalid patient ID. Please enter a numeric value.")
                            elif choice == 3:
                                print("Exiting...")
                                break
                            else:
                                print("Invalid choice. Please enter a number between 1 and 3.")
                        except ValueError:
                            print("Invalid input. Please enter a number for your choice.")
                elif choice == 6:
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 4.")
            except ValueError as e:
                # Handle invalid input type
                print(f"Invalid input. Please enter a valid number. Error: {e}")
    else:
        print("Invalid admin credentials. Please try again.")


# Main Menu Options
def main_menu(user):
    user_id, user_type = user
    while True:
        print("\nMain Menu")
        if user_type == 'patient':
            print("1. Book Appointment")
            print("2. Pay Bill")
            print("3. Display Doctor List")
            print("4. Display Token")
            print("5. Fill Your Details")
            print("6. Display user details")
            print("7. View your profile")
            print("8. View hospital branch")
            print("9. Logout")
            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    search_specialization()
                    specialization_choice = int(input("Enter your choice: "))
                    display_doctor_specialization(specialization_choice)
                    user_id = int(input("Enter the patient ID: "))
                    doctor_id = int(input("Enter the doctor ID: "))
                    hospital_id = int(input("Enter the hospital ID: "))
                    appointment_date = input("Enter appointment date (YYYY-MM-DD HH:MM:SS): ")
                    book_appointment(user_id, doctor_id, hospital_id, appointment_date)
                elif choice == 2:
                    patient_id = int(input("Enter the patient ID: "))
                    amount = float(input("Enter the amount: "))
                    hospital_id = int(input("Enter the hospital ID: "))
                    pay_bill(patient_id, hospital_id, amount)
                elif choice == 3:
                    while True:
                        print("\nDoctor List Options:")
                        print("1. Display All Doctors")
                        print("2. Display Doctors by Specialization")
                        print("3. Display Doctors by Name")
                        print("4. Exit")
                        list_choice = input("Enter your choice (1-4): ")
                        if list_choice == '1':
                            display_doctor_list()
                        elif list_choice == '2':
                            search_specialization()
                            specialization_choice = int(input("Enter your choice: "))
                            display_doctor_specialization(specialization_choice)
                        elif list_choice == '3':
                            name_filter = input("Enter name or partial name: ")
                            display_doctor_list('name', name_filter)
                        elif list_choice == '4':
                            print("Exiting...")
                            break
                        else:
                            print("Invalid choice. Please enter a number between 1 and 4.")
                elif choice == 4:
                    patient_id = int(input("Enter patient ID: "))
                    display_token(patient_id)
                elif choice == 5:
                    user_type = input("Enter user type (patient/doctor/admin): ")
                    user_id = input("Enter user_id: ")
                    Fill_details(user_type, user_id)
                elif choice ==6:
                    username=input("enter your username: ")
                    view_user_dp(username)
                elif choice ==7:
                    try:
                        patient_id = int(input("Enter the patient ID: "))
                        view_patient(patient_id)
                    except ValueError:
                        print("Invalid patient ID. Please enter a numeric value.")
                elif choice ==8:
                    get_hospital()
                elif choice == 9:
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError as e:
                print(f"Invalid input. Please enter a valid number. Error: {e}")

        elif user_type == 'doctor':
            print("1. View Appointments")
            print("2. View user details")
            print("3. Update Token Status")
            print("4. Fill Your Details")
            print("5. Display Profile")
            print("6. Logout")
            
            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    user_id = int(input("Enter doctor ID: "))
                    view_appointments(user_id)
                elif choice ==2:
                    username=input("enter your username: ")
                    view_user_dp(username)
                elif choice == 3:
                    token_id = int(input("Enter token ID: "))
                    status = input("Enter status (completed/pending): ")
                    if status not in ['completed', 'pending']:
                        print("Invalid status. Please enter 'completed' or 'pending'.")
                    else:
                        update_token_status(token_id, status)
                elif choice == 4:
                    user_type = input("Enter user type (doctor): ")
                    user_id = input("Enter user_id: ")
                    Fill_details(user_type, user_id)
                elif choice == 5:
                    doctor_id=int(input("Enter the Id: "))
                    doctor_profile(doctor_id)
                elif choice == 6:
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError as e:
                print(f"Invalid input. Please enter a valid number. Error: {e}")
  

if __name__ == "__main__":
    while True:
        print("1. Sign Up")
        print("2. Log In")
        print("3. Log In Admin")
        print("4. Create hospital database")
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                username = input("Create username: ")
                password = input("Create password: ")
                user_type = input("Enter user type (patient/doctor): ")
                signup_user(username, password, user_type)
            elif choice == 2:
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = login_user(username, password)
                if user:
                    main_menu(user)
            elif choice == 3:
                username = input("Enter username: ")
                password = input("Enter password: ")
                admin_user(username, password)
            elif choice == 4:
                hospital_id = int(input("Enter hospital id: "))
                name = "Jila_hospital"
                address = input("Enter address: ") 
                phone = input("Enter phone number: ")
                email = input("Enter email: ")
                ensure_default_hospital(hospital_id, name, address, phone, email)
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number for your choice.")