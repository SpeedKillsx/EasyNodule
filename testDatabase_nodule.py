import numpy as np
import datetime
import sqlite3
import matplotlib.pyplot as plt
Database_path = "NoduleDatabase.db"
#! Research a nodule
def NoduleResearch(ConsultationID):
    exist = -1
    request_research = "SELECT * FROM Nodule where idConsultation = ?"
    #* Create a connection
    conn = sqlite3.connect(Database_path)
    cursor = conn.cursor()
    cursor.execute(request_research, ( ConsultationID, ))
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
    if NoduleResearch(ConsultationID) == -1 and CoupleExiste(ConsultationID, PatientID) == 1: #! The nodule doesn't existe
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
            print("This patient never passed this consultation, please check the ID of the patient or of the consultation")
        else:
            print("The nodule already exist")
#? Search for a nodule if he exists
def SelectNodule(ConsultationID):
    request_research = "SELECT NoduleArray FROM Nodule where idConsultation = ?"
    if NoduleResearch(ConsultationID) == 1:
        conn = sqlite3.connect(Database_path)
        cursor = conn.cursor()
        cursor.execute(request_research, (ConsultationID, ))
        result = cursor.fetchone()[0]
        conn.close()
        img = np.fromstring(result,dtype='float32').reshape(64,64,1)
        plt.imshow(img, "gray")
        plt.show()
        
def NoduleModify(PatientID, ConsultationID, NoduleArray, NoduleClassification):
    update_request = "UPDATE Nodule set idP = ?, NoduleArray = ? , NoduleClassification = ? where idConsultation = ?"
    #? Check if the nodule existe
    if NoduleResearch(ConsultationID) == 1:
        #* Prepare the nodule img
        array_str = NoduleArray.tostring()
        #! The nodule existe
        conn = sqlite3.connect(Database_path)
        cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            cursor.execute(update_request, (PatientID, sqlite3.Binary(array_str), NoduleClassification, ConsultationID))
            if cursor.rowcount <1:
                print("Can't Update the nodule")
            else:
                print("Nodule Updated")
            conn.commit()
            conn.close()
        except:
            print("Check if the consultation ID or patient ID are correct")
        
if __name__ =="__main__":
    #NoduleResearch('P000', 'CS000')
    test = np.load('XTrain_X_aug.npy', allow_pickle=True)
    NoduleInsert('CS005', 'P004', test[4],0)
    #SelectNodule('CS003')
    #NoduleModify('P003', 'CS003', test[25], 1)

    
    