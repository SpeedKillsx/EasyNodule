import sqlite3
import datetime
from multipledispatch import dispatch
Database_path = "NoduleDatabase.db"
#==============================================================================================================
#                                                           CLINICIAN
#==============================================================================================================
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
    select_request = "SELECT NameC, BirthdayC, WilayaC, Hospital, Grade, PasswordC, UsernameC, idC from Clinician where idC = ?" 
    cursor.execute(select_request, (IDClinian, ))
    clinician_actual_info = [info for info in cursor.fetchall()[0]]
    """
        Here we change the fields in the interface
        self.NameC, self.BirthdayC, self.WilayaC, self.Hospital, self.Grade, self.PasswordC, self.UsernameC = self.clinician_actual_info
    """
    NameC, BirthdayC, WilayaC,Hospital, Grade, PasswordC, UsernameC, idC = clinician_actual_info
    return NameC, BirthdayC, WilayaC,Hospital, Grade, PasswordC, UsernameC, idC


#? Get Clinician ID
def ClinicianID(ClinicianUsername):
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
    search_request = "SELECT idC from Clinician where UsernameC = ?"
    exist = -1
    conn = sqlite3.connect(Database_path)
    
    #! Create a curson for the request
    cursor = conn.cursor()
    #! Execute the request
    cursor.execute(search_request, (ClinicianUsername, ))
    #* Check if there is a resulted row
    data = cursor.fetchone()
    
    conn.close()
    return data
#==============================================================================================================
#                                                           PATIENT
#==============================================================================================================
#? Methode that search for a patient
def PatientResearchPhoneName(PhonePatient,NamePatient):
    """
    Search if a patient with a given Patient's Email and Patient's Name existe in the database
    Args:
        PhonePatient (str): The phone number of the patient\n
        NamePatient  (str): The name of the patient

    Returns:
        int: 1 if the patient existe else -1
    """
    #! The request below select an ID from table clinician
    search_request = "SELECT * from Patient where PhoneP = ? and NameP = ?"
    exist = -1
    conn = sqlite3.connect(Database_path)
    print ("Opened database successfully")
    #! Create a curson for the request
    cursor = conn.cursor()
    #! Execute the request
    cursor.execute(search_request, (PhonePatient,NamePatient))
    #* Check if there is a resulted row
    data = cursor.fetchone()
    if data is None:
        #! Case where there is no patient with the given Name
        print("There is no patient with this Name!!!\nPlease, check again if there are no mistakes in the identifiant")
    else:
        exist = 1
    conn.close()
    return exist

#? Methode that search for a patient
def PatientInfoByPhoneName(PhonePatient,NamePatient):
    """
    Search if a patient with a given Patient's Email and Patient's Name existe in the database
    Args:
        PhonePatient (str): The phone number of the patient\n
        NamePatient  (str): The name of the patient

    Returns:
        int: 1 if the patient existe else -1
    """
    #! The request below select an ID from table clinician
    search_request = "SELECT * from Patient where PhoneP = ? and NameP = ?"
    search_request_all = "SELECT * from Patient"
    conn = sqlite3.connect(Database_path)
    print ("Opened database successfully")
    #! Create a curson for the request
    cursor = conn.cursor()
    #! Execute the request
    cursor.execute(search_request, (PhonePatient,NamePatient))
    #* Check if there is a resulted row
    data = cursor.fetchone()
    if data is not None:
        idP,NameP, BirthdayP, WilayaP, Gender, Allergies, Smoking,MedHistroy, CancerFamilly, EmailP, PhoneP  =  data
    else:
        cursor = conn.cursor()
        #! Execute the request
        cursor.execute(search_request_all, ())
        data = cursor.fetchall()
    conn.close()
    
    return data

def CreateIdp():
    """
    Create an automatic ID for a new patient if he doesn't exist already in the database.
    The new ID can be in one of the 3 categories:
        Category 1: The patient was added with the 10th first patient in the app, the ID would be between P000 and P009
        Category 2: The patient was added with the 100th first patient in the app, the ID would be between P010 and P099
        Category 3: The patient was added the rest of possible IDs in the App, the ID would be between P0100 and PXXX
    Returns:
        str: the new ID
    """
    request_all_IDs = "SELECT idP from Patient"
    #! Connect to the database
    conn = sqlite3.connect(Database_path)
    cursor= conn.cursor()
    cursor.execute(request_all_IDs)
    datas = cursor.fetchall()
    
    #! Auto-Incerement the ID
    #print(datas[-1])
    if len(datas) == 0:
        actula_id = "P000"
        return actula_id
    actula_id = int(datas[-1][-1].strip('P'))
    new_id = actula_id + 1
    #* Check in which categroy the ID should be in :
    
    if len(str(new_id)) == 1 and new_id !=10: #!First Category P00X
        new_id = str('P00') + str(new_id)
    elif len(str(new_id)) == 2 and new_id !=100: #* Second Category P0XX
        new_id = str('P0') + str(new_id)
    else: #? Third Category PXXX or more
        new_id = str('P') + str(new_id)
    
    conn.close()
    return new_id

#? Methode that search for a patient
def PatientResearchPhoneName(PhonePatient,NamePatient ):
    """
    Search if a patient with a given Patient's Email and Patient's Name existe in the database
    Args:
        PhonePatient (str): The phone number of the patient\n
        NamePatient  (str): The name of the patient

    Returns:
        int: 1 if the patient existe else -1
    """
    #! The request below select an ID from table clinician
    search_request = "SELECT * from Patient where PhoneP = ? and NameP = ?"
    exist = -1
    conn = sqlite3.connect(Database_path)
    print ("Opened database successfully")
    #! Create a curson for the request
    cursor = conn.cursor()
    #! Execute the request
    cursor.execute(search_request, (PhonePatient,NamePatient))
    #* Check if there is a resulted row
    data = cursor.fetchone()
    
    if data is None:
        #! Case where there is no patient with the given Name
        print("There is no patient with this Name!!!\nPlease, check again if there are no mistakes in the identifiant")
    else:
        exist = 1
    conn.close()
    return exist

#? Methode that insert for a patient
def PatientInsert(NameP,BirthdayP,WilayaP,Sexe,Allergies,Smoking,MedHistory,CancerFamilly,EmailP,PhoneP):
    """Insert a new patient in the database. If the patient has already an account, the account can't be created.

    Args:
        NameP (_type_): Name of the patient\n
        BirthdayP (_type_): Birthday of the patient\n
        WilayaP (_type_): Wilaya of the patient\n
        Sexe (_type_): Sexe of the patient\n
        Allergies (_type_): Allergies of the patient\n
        Smoking (_type_): a bool that indicates if the patient smook or not\n
        MedHistory (_type_): Medical history of the patient\n
        CancerFamilly (_type_): A bool, it indicates if there is a member of the familly affected by lung cancer\n
        EmailP (_type_): email of the patient\n
        PhoneP (_type_): Number phone of the patient\n
    """
    if PhoneP=="" or NameP=="":
        print("Please insert a phone number and Name!!!")
        return
    if PatientResearchPhoneName(PhoneP, NameP) == 1:
        print("Cannot Create this account, because this patient already exist in the database")
    else:
        #! Request to insert new clinician in the database
        insert_request = "INSERT INTO Patient (idP, NameP,BirthdayP,WilayaP,Sexe,Allergies,Smoking,MedHistory,CancerFamilly,EmailP,PhoneP) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        #! Create an ID for the new clinician
        idC = CreateIdp()
        birth = BirthdayP.split('/')
        
        day = int(birth[0])
        month = int(birth[1])
        year  = int(birth[2])
        
        #! Connect the database
        conn = sqlite3.connect(Database_path)
        cursor = conn.cursor()
        cursor.execute(insert_request, (idC, NameP,datetime.date(year, month, day),WilayaP,Sexe,Allergies,Smoking,MedHistory,CancerFamilly,EmailP,PhoneP))
        conn.commit()
        conn.close()
        print("Patient added")
#? This method is to search a patient using his ID
def PatientSearchByID(PatientID):
    exit = -1
    request_searchID = "SELECT *  From Patient where idP = ?"
    conn = sqlite3.connect(Database_path)
    cursor = conn.cursor()
    cursor.execute(request_searchID,(PatientID, ))
    data = cursor.fetchone()
    print(data)
    
    if data == None:
        print("There is no patient with this identifiant!!!\nPlease check if the ID is correct")
    else:
        exit = 1
    conn.close()
    return exit

#? This method is to modify the information of a patient
def PatientModify(idP, NameP,BirthdayP,WilayaP,Sexe,Allergies,Smoking,MedHistory,CancerFamilly,EmailP,PhoneP):
    if PatientSearchByID(idP) == 1:
        #! Connect to the database
        conn = sqlite3.connect(Database_path)
        cursor = conn.cursor()
        update_request = "UPDATE Patient set NameP = ?,BirthdayP = ?,WilayaP = ?,Sexe = ?,Allergies = ?,Smoking = ?,MedHistory = ?,CancerFamilly = ?,EmailP = ?,PhoneP = ? where idP = ?"
        birth = BirthdayP.split('/')
        day = int(birth[0])
        month = int(birth[1])
        year  = int(birth[2])
        BirthdayP = datetime.date(year, month, day)
        cursor.execute(update_request, (NameP,BirthdayP,WilayaP,Sexe,Allergies,Smoking,MedHistory,CancerFamilly,EmailP,PhoneP, idP))
        conn.commit()
        conn.close()
        print("Patient update succesfully")