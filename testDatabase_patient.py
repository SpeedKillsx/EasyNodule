import sqlite3
import datetime
Database_path = "NoduleDatabase.db"

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
        NameP (_type_): Name of the patient
        BirthdayP (_type_): Birthday of the patient
        WilayaP (_type_): Wilaya of the patient
        Sexe (_type_): Sexe of the patient
        Allergies (_type_): Allergies of the patient
        Smoking (_type_): a bool that indicates if the patient smook or not
        MedHistory (_type_): Medical history of the patient
        CancerFamilly (_type_): A bool, it indicates if there is a member of the familly affected by lung cancer
        EmailP (_type_): email of the patient
        PhoneP (_type_): Number phone of the patient
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
#==================================================================TEST==========================================================================
#================================================================================================================================================
#! An exemple of the insert method
"""patients = [    ['Yasmine Ait Bouhaddou', '15/02/1987', 'Bejaia', 'Female', 'Arachide', 0, 'Hypertension', 0, 'yasmine@example.com', '0555123456'],
    ['Khalil Benamar', '23/08/1975', 'Alger', 'Male', 'None', 1, 'Diabete, Asthme', 1, 'khalil@example.com', '0666123456'],
    ['Nour El Imane Meziani', '29/11/1999', 'Tizi Ouzou', 'Female', 'Poussiere, Acariens', 0, 'Migraine', 0, 'nour@example.com', '0555765432'],
    ['Moussa Djelloul', '10/06/1960', 'Oran', 'Male', 'None', 0, 'Cholesterol', 1, 'moussa@example.com', '0799123456'],
    ['Fatima Zohra Djabali', '07/03/1981', 'Annaba', 'Female', 'Aspirine', 0, 'None', 1, 'fatima@example.com', '0567123456']
]
for p in patients:
    NameP,BirthdayP,WilayaP,Sexe,Allergies,Smoking,MedHistory,CancerFamilly,EmailP,PhoneP = p
    PatientInsert(NameP,BirthdayP,WilayaP,Sexe,Allergies,Smoking,MedHistory,CancerFamilly,EmailP,PhoneP)"""
    
"""
Marche
#! An exemple of the update method
PatientModify('P002','Nour El Imane Meziani', '29/11/1999', 'Tizi Ouzou', 'Female', 'Acariens', 0, 'None', 0, 'nour@example.com', '0555765432')
"""
#PatientSearchByID('P04')
#PatientInsert('Nour El Imane Meziani', '29/11/1999', 'Tizi Ouzou', 'Male', 'Poussiere, Acariens', 0, 'Migraine', 0, 'nour@example.com', '0555765432')
#PatientModify('P002','Nour El Imane Meziani', '29/11/1999', 'Tizi Ouzou', 'Female', 'Acariens, Poussiere', 0, 'None', 0, 'nour@example.com', '0555765432')
PatientInsert('Patient', '29/11/1999', 'Tizi Ouzou', 'Male', 'Poussiere, Acariens', 0, 'Migraine', 0, 'nour@example.com', '0555765432')