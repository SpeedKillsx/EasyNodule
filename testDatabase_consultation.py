import sqlite3
import datetime


Database_path = "NoduleDatabase.db"
#* Method Auto Increment the ConsultationID
def CreateIdConsultation():
    """
    Create an automatic ID for a new patient if he doesn't exist already in the database.
    The new ID can be in one of the 3 categories:
        Category 1: The Consultation was added with the 10th first Consultation in the app, the ID would be between CS000 and CS009
        Category 2: The Consultation was added with the 100th first Consultation in the app, the ID would be between CS010 and CS099
        Category 3: The Consultation was added the rest of possible IDs in the App, the ID would be between P0100 and CSXXX
    Returns:
        str: the new ID
    """
    request_all_IDs = "SELECT idConsultation from Consultation"
    #! Connect to the database
    conn = sqlite3.connect(Database_path)
    cursor= conn.cursor()
    cursor.execute(request_all_IDs)
    datas = cursor.fetchall()
    #! Auto-Incerement the ID
    #print(datas[-1])
    if len(datas) == 0:
        actula_id = "CS000"
        return actula_id
    actula_id = int(datas[-1][-1].strip('CS'))
    new_id = actula_id + 1
    #* Check in which categroy the ID should be in :
    if len(str(new_id)) == 1 and new_id !=10: #!First Category P00X
        new_id = str('CS00') + str(new_id)
    elif len(str(new_id)) == 2 and new_id !=100: #* Second Category P0XX
        new_id = str('CS0') + str(new_id)
    else: #? Third Category PXXX or more
        new_id = str('CS') + str(new_id)
    
    conn.close()
    return new_id
#* Method search consultation using the ID
def SearchConsultation(ClincianID, PatientID, DateConsultation):
    exist = -1
    request_search = "SELECT * FROM Consultation where idC =? and idP = ? and DateConsultation = ?"
    #! Change the format of the date (from dd/mm/yy to yy/mm/dd )
    DateConsultation = DateConsultation.replace('/','-')
    day, month, year = DateConsultation.split('-')
    DateConsultation = datetime.date(int(year), int(month), int(day))
    #DateConsultation = year+month+day
    
    #! Create a connection to the database
    conn = sqlite3.connect(Database_path)
    cursor = conn.cursor()
    #* Execute the request
    cursor.execute(request_search, (ClincianID, PatientID, DateConsultation))
    #! take result of execution, we know that we will have just one row
    data = cursor.fetchone()
    #! Check if there is a row
    if data is None:
        print("There is no consultation with this id\n")
    else:
        print("The consultation already exist")
        exist = 1
    conn.close()
    return exist

#! Insert a new consultation in the database
def ConsultationInsert(ClinicianID, PatientID, DateConsultation, MedicalObservation):
    """Insert a new consultation in the database

    Args:
        ClinicianID (str): ID of the Clinician
        PatientID (str): ID of the patient
        DateConsultation (str): Date fo the consultation
    """
    request_insert="INSERT INTO Consultation (idConsultation, idC, idP, DateConsultation, MedicalObservation) Values(?,?,?,?,?)"
    
    #? Check if the consultation exist
    if SearchConsultation(ClinicianID,PatientID, DateConsultation) == -1: #* The consultation doesn't existe
        #! Create a connection to the database
        conn = sqlite3.connect(Database_path)
        conn.execute("PRAGMA foreign_keys = ON")
        #* Create a cursor
        cursor = conn.cursor()
        #! Create a new ConsultationID
        ConsultationID = CreateIdConsultation()
        #! Split the date
        day, month, year = DateConsultation.split('/')
        try:
            cursor.execute(request_insert, (ConsultationID, ClinicianID, PatientID, datetime.date(int(year), int(month), int(day)), MedicalObservation))
            conn.commit()
            print("Consultation is added")
        except:
            print("There is a mistake in the information, check if Consultation's ID or Patient's ID are correct!!!!")       
        conn.close()
#! Show all the consultation for a patient
def PatientConsultation(PatientID):
    data = None
    request_consultations = "SELECT * FROM Consultation where idP = ?"
    #! Create a connection
    conn = sqlite3.connect(Database_path)
    cursor = conn.cursor()
    cursor.execute(request_consultations, (PatientID, ))
    
    data = cursor.fetchall()
    conn.close()
    if data is None:
        print("There is no consultation for this patient")
    
    return data
def ConsultationModify(ConsultationID, ClinicianID,PatientID, DateConsultation, MedicalObservation):
    #* Check if the connection existe
    #! The consultation existe, we can modify it
    update_request = "UPDATE Consultation set idC = ?,idP = ?, DateConsultation = ?, MedicalObservation = ? where idConsultation = ?"
    conn = sqlite3.connect(Database_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA primary_keys = ON")
    day, month, year = DateConsultation.split('/')
    cursor = conn.cursor()
    try:
        cursor.execute(update_request, (ClinicianID, PatientID, datetime.date(int(year), int(month), int(day)),MedicalObservation, ConsultationID))
        conn.commit()
        if cursor.rowcount < 1:
            print("There is no consultation with this ID, please check your identifiant")
        else:
            print("Consultation Updated")
    except sqlite3.IntegrityError:
        print("Verify if your id/patient's ID are correct")
    conn.close()
    #print("Check the your ID or the ID of the patient.")
if __name__ =="__main__":
    
    """
    ! Les fonction qui marchent :
        - SearchConsultation("CS000")
        - CreateIdConsultation()
        - ConsultationInsert('C000', 'P2001','20/05/2020')
        - PatientConsultation('P000')
    """
    #ConsultationInsert('C024', 'P005','2/08/2020')
    #print(PatientConsultation('P000'))
    ConsultationModify('CS001','C000', 'P001','2/08/2020', 'Very Good tests')
    

    


