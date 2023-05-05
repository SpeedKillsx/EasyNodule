import numpy as np
import datetime
import sqlite3
import matplotlib.pyplot as plt
Database_path = "NoduleDatabase.db"
#! Research a nodule
def NoduleResearch(PatientID, ConsultationID):
    exist = -1
    request_research = "SELECT * FROM Nodule where idP = ? and idConsultation = ?"
    #* Create a connection
    conn = sqlite3.connect(Database_path)
    cursor = conn.cursor()
    cursor.execute(request_research, (PatientID, ConsultationID))
    data = cursor.fetchone()
    
    if data is None:
        print("The nodule doesn't exist")
    else:
        exist = 1
    conn.close()
    return exist
#? Check if a consultation was done for a patient
def CoupleExiste(ConsultationID, PatientID):
    """Check if the patient with the given ID has passd this consultation

    Args:
        ConsultationID (str): ID of the consultation
        PatientID (str): Id of the patient

    Returns:
        int: Integer Value, 1 if the patient passed the consultation, if not return -1
    """
    request_research = "SELECT * FROM Consultation where idP = ? and idConsultation = ?"
    conn = sqlite3.connect(Database_path)
    cursor = conn.cursor()
    cursor.execute(request_research, (PatientID, ConsultationID))
    result = cursor.fetchone()
    #print("Le resultat = ", result)
    if result is None:
        conn.close()
        return -1
    else:
        conn.close()
        return 1
#? Insert a nodule in the database
def NoduleInsert(ConsultationID, PatientID, NoduleArray, NoduleClassification):
    request_insert = "INSERT INTO Nodule (idConsultation, idP, NoduleArray, NoduleClassification) VALUES (?,?,?,?)"
    if NoduleResearch(PatientID, ConsultationID) == -1 and CoupleExiste(ConsultationID, PatientID) == 1: #! The nodule doesn't existe
        conn = sqlite3.connect(Database_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        #* Convert numpy array to string
        array_str = NoduleArray.tostring()
        try:
            cursor.execute(request_insert, (ConsultationID, PatientID, sqlite3.Binary(array_str), NoduleClassification))
            conn.commit()
        except:
            print("Check if the consultation ID or patient ID are correct")
        
        conn.close()
    else:
        if CoupleExiste(ConsultationID, PatientID) == -1:
            print("There is no consultation for this patient done by this clinician")
        else:
            print("The nodule already exist")
#? Search for a nodule if he exists
def SelectNodule(ConsultationID, PatientID):
    request_research = "SELECT NoduleArray FROM Nodule where idP = ? and idConsultation = ?"
    if NoduleResearch(PatientID, ConsultationID) == 1:
        conn = sqlite3.connect(Database_path)
        cursor = conn.cursor()
        cursor.execute(request_research, (PatientID, ConsultationID))
        result = cursor.fetchone()[0]
        conn.close()
        img = np.fromstring(result,dtype='float32').reshape(64,64,1)
        plt.imshow(img, "gray")
        plt.show()
        
    
if __name__ =="__main__":
    #NoduleResearch('P000', 'CS000')
    test = np.load('XTrain_X_aug.npy', allow_pickle=True)
    #NoduleInsert('CS003', 'P003', test[4],0)
    SelectNodule('CS003', 'P003')

    
    