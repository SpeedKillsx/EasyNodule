import sqlite3
import datetime
import os
#? Metod to generate a new ID for the Clinician
def CreateIdc():
    request_all_IDs = "SELECT idC from Clinician"
    #! Connect to the database
    conn = sqlite3.connect("NoduleDatabase.db")
    cursor= conn.cursor()
    cursor.execute(request_all_IDs)
    datas = cursor.fetchall()
    print(datas[-1])
    actula_id = int(datas[-1][-1].strip('C'))
    new_id = actula_id + 1
    if len(str(new_id)) == 1 and new_id !=10:
        new_id = str('C00') + str(new_id)
    elif len(str(new_id)) == 2 and new_id !=100:
        new_id = str('C0') + str(new_id)
    else:
        new_id = str('C') + str(new_id)
    
    conn.close()
    
    return new_id
#? Methode that search for a clinician
def ClinicianResearch(ClinicianUsername):
    #! The request below select an ID from table clinician
    search_request = "SELECT idC from Clinician where UsernameC = ?"
    exist = -1
    conn = sqlite3.connect('NoduleDatabase.db')
    print ("Opened database successfully")
    #! Create a curson for the request
    cursor = conn.cursor()
    #! Execute the request
    cursor.execute(search_request, (ClinicianUsername, ))
    #* Check if there is a resulted row
    data = cursor.fetchone()
    
    if data is None:
        #! Case where there is no clinician with the given Name
        print("There is no clinician with this Name!!!\nPlease, check again if there are no mistakes in the identifiant")
    else:
        exist = 1
    conn.close()
    return exist
#? Method for inserting a new clinician in the database
def ClinicianInsert(NameC, BirthdayC, WilayaC, Hospital, Grade, PasswordC, UsernameC):
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
        conn = sqlite3.connect('NoduleDatabase.db')
        cursor = conn.cursor()
        cursor.execute(insert_request, (idC, NameC,datetime.date(year, month, day),WilayaC, Hospital, Grade, PasswordC, UsernameC))
        conn.commit()
        conn.close()
#ClinicianResearch('C000')
ClinicianInsert("KOULAL Yidhir Aghiles","1/3/2000", 'Tizi-Ouzou','Meghnem Lounes','Pr','1234', 'Y1D1R')
#CreateIdc()