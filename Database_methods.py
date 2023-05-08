import sqlite3
import datetime
from multipledispatch import dispatch
Database_path = "NoduleDatabase.db"
#? Metod to generate a new ID for the Clinician
def CreateIdc():
    """
    Create an automatic ID for a new clinician if he doesn't exist already in the database.
    The new ID can be in one of the 3 categories:
        Category 1: The clinician signed up with the 10th first clinician in the app, the ID would be between C000 and C009
        Category 2: The clinician signed up with the 100th first clinician in the app, the ID would be between C010 and C099
        Category 3: The clinician will have the rest of possible IDs in the App, the ID would be between C0100 and CXXX
    Returns:
        str: the new ID
    """
    request_all_IDs = "SELECT idC from Clinician"
    #! Connect to the database
    conn = sqlite3.connect(Database_path)
    cursor= conn.cursor()
    cursor.execute(request_all_IDs)
    datas = cursor.fetchall()
    
    #! Auto-Incerement the ID
    #print(datas[-1])
    if len(datas) == 0:
        actula_id = "C000"
        return actula_id
    actula_id = int(datas[-1][-1].strip('C'))
    new_id = actula_id + 1
    #* Check in which categroy the ID should be in :
    
    if len(str(new_id)) == 1 and new_id !=10: #!First Category C00X
        new_id = str('C00') + str(new_id)
    elif len(str(new_id)) == 2 and new_id !=100: #* Second Category C0XX
        new_id = str('C0') + str(new_id)
    else: #? Third Category CXXX or more
        new_id = str('C') + str(new_id)
    
    conn.close()
    
    return new_id
#? Methode that search for a clinician
@dispatch(str)
def ClinicianResearch(ClinicianUsername):
    """
    Search if a clinician with a given username existe in the database
    Args:
        ClinicianUsername (str): The username of the patient

    Returns:
        int: 1 if the patient existe else -1
    """
    print("function one")
    #! The request below select an ID from table clinician
    search_request = "SELECT idC from Clinician where UsernameC = ?"
    exist = -1
    conn = sqlite3.connect(Database_path)
    #print ("Opened database successfully")
    #! Create a curson for the request
    cursor = conn.cursor()
    #! Execute the request
    cursor.execute(search_request, (ClinicianUsername, ))
    #* Check if there is a resulted row
    data = cursor.fetchone()
    
    if data is not  None:
        #! Case where there is no clinician with the given Name
        exist = 1
    conn.close()
    return exist
#? Connect 
@dispatch(str, str)
def ClinicianResearch(ClinicianUsername, ClinicianPassword):
    """
    Search if a clinician with a given username and passworf existe in the database
    Args:
        ClinicianUsername (str): The username of the patient
        ClinicianPassword (str): Password of the clinician 
    Returns:
        int: 1 if the patient existe else -1
    """
    print("function two")
    #! The request below select an ID from table clinician
    search_request = "SELECT idC from Clinician where UsernameC = ? and PasswordC = ?"
    exist = -1
    conn = sqlite3.connect(Database_path)
    
    #! Create a curson for the request
    cursor = conn.cursor()
    #! Execute the request
    cursor.execute(search_request, (ClinicianUsername,ClinicianPassword ))
    #* Check if there is a resulted row
    data = cursor.fetchone()
    
    if data is not None:
        exist = 1
    conn.close()
    return exist
#? Method for inserting a new clinician in the database
def ClinicianInsert(NameC, BirthdayC, WilayaC, Hospital, Grade, PasswordC, UsernameC):
    """Insert a new clinician in the database. If the clinician has already an account, the account can't be created.

    Args:
        NameC (str): Name of the clinician\n
        BirthdayC (Date): Clinician's birthday\n
        WilayaC (str): Wilaya of residence\n
        Hospital (str): Hospital where the clinician work\n
        Grade (str): Grade of the clinician\n
        PasswordC (str): Password introduced by the clinician\n
        UsernameC (str): Username introduced by the clinician\n
    """
    if ClinicianResearch(UsernameC) == 1:
        print("Cannot Create this account, because this clinician already exist in the database")
    else:
        
        #! Request to insert new clinician in the database
        insert_request = "INSERT INTO Clinician (idC, NameC, BirthdayC, WilayaC, Hospital, Grade, PasswordC, UsernameC) VALUES (?,?,?,?,?,?,?,?)"
        #! Create an ID for the new clinician
        idC = CreateIdc()
        birth = BirthdayC.split('/')
        
        day = int(birth[0])
        month = int(birth[1])
        year  = int(birth[2])
        
        #! Connect the database
        conn = sqlite3.connect(Database_path)
        cursor = conn.cursor()
        cursor.execute(insert_request, (idC, NameC,datetime.date(year, month, day),WilayaC, Hospital, Grade, PasswordC, UsernameC))
        conn.commit()
        conn.close()
#? This method is to modify the information of a clinician
def ClinicianModify(idC, NameC, BirthdayC, WilayaC, Hospital, Grade, PasswordC, UsernameC):
    if ClinicianResearch(UsernameC) == 1:
        conn = sqlite3.connect(Database_path)
        cursor = conn.cursor()
        update_request = "UPDATE Clinician set NameC = ?, BirthdayC = ?, WilayaC = ?, Hospital = ?, Grade = ?, PasswordC = ?, UsernameC = ? where idC = ?"
        birth = BirthdayC.split('/')
        day = int(birth[0])
        month = int(birth[1])
        year  = int(birth[2])
        BirthdayC = datetime.date(year, month, day)
        cursor.execute(update_request, (NameC, BirthdayC, WilayaC, Hospital, Grade, PasswordC, UsernameC, idC))
        conn.commit()
        conn.close()
        print("Clinician Updated")
    else:
        print("Can't update a user that doesn't exist!!!!\nCheck your username")
        
#? Delete Clinician
def ClinicianDelete(UsernameClinician):
    delete_request = "DELETE FROM Clinician where UsernameC = ?"
    if ClinicianResearch(UsernameClinician) == 1:
        conn = sqlite3.connect(Database_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute(delete_request, (UsernameClinician, ))
        conn.commit()
        conn.close()
        print('Account is deleted')
    else:
        print("There no account with this username")
#? This method is to write the actual information of a clinician, we can use it in the interface
def PrintActualClinicianInfo(IDClinian):
    #*Create a connection to the database
    conn = sqlite3.connect(Database_path)
    cursor = conn.cursor()
    #* Request to select all cilinician's information
    select_request = "SELECT NameC, BirthdayC, WilayaC, Hospital, Grade, PasswordC, UsernameC from Clinician where idC = ?" 
    cursor.execute(select_request, (IDClinian, ))
    clinician_actual_info = [info for info in cursor.fetchall()[0]]
    """
        Here we change the fields in the interface
        self.NameC, self.BirthdayC, self.WilayaC, self.Hospital, self.Grade, self.PasswordC, self.UsernameC = self.clinician_actual_info
    """
#=================================================PATIENT=====================================================
