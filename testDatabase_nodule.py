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

def NoduleInsert(ConsultationID, PatientID, NoduleArray, NoduleClassification):
    request_insert = "INSERT INTO Nodule (idConsultation, idP, NoduleArray, NoduleClassification) VALUES (?,?,?,?)"
    if NoduleResearch(PatientID, ConsultationID) == -1: #! The nodule doesn't existe
        conn = sqlite3.connect(Database_path)
        cursor = conn.cursor()
        #* Convert numpy array to string
        array_str = NoduleArray.tostring()
        cursor.execute(request_insert, (ConsultationID, PatientID, sqlite3.Binary(array_str), NoduleClassification))
        conn.commit()
        conn.close()
    else:
        print("The nodule already exist")
def SelectNodule(ConsultationID, PatientID):
    request_research = "SELECT NoduleArray FROM Nodule where idP = ? and idConsultation = ?"
    if NoduleResearch(ConsultationID, PatientID) ==1:
        conn = sqlite3.connect(Database_path)
        cursor = conn.cursor()
        cursor.execute(request_research, (ConsultationID, PatientID))
        result = cursor.fetchone()[0]
        conn.close()
        img = np.fromstring(result,dtype='float32').reshape(64,64,1)
        plt.imshow(img, "gray")
        plt.show()
        
    
if __name__ =="__main__":
    #NoduleResearch('P000', 'CS000')
    test = np.load('XTrain_X_aug.npy', allow_pickle=True)
    #NoduleInsert('P000', 'CS000', test[0],1)
    SelectNodule('CS000', 'P000')

    
    