import sqlite3
import datetime
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
def ClinicianResearch(ClinicianUsername):
    """
    Search if a clinician with a given username existe in the database
    Args:
        ClinicianUsername (str): The username of the patient

    Returns:
        int: 1 if the patient existe else -1
    """
    #! The request below select an ID from table clinician
    search_request = "SELECT idC from Clinician where UsernameC = ?"
    exist = -1
    conn = sqlite3.connect(Database_path)
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
    
#ClinicianResearch('C000')
#ClinicianInsert("KOULAL Yidhir Aghiles","1/3/2000", 'Tizi-Ouzou','Meghnem Lounes','Pr','1234', 'Y1D1R')
#CreateIdc()
#ClinicianModify("C001", "Labchri Amayas","8/8/2000", 'Algiers','Mustapha Bacha','Pr','1234', 'SpeedKillsx')
"""v = [
('Bouchama Benamar', '06/04/1978', 'Tipaza', 'CHU de Blida', 'Radiologue', 'f5G5c&X2e', 'bouchama_benamar'),
('Ouyahia Nabil', '24/09/1985', 'Setif', 'EPH de Jijel', 'Pneumologue', 'h4G7p@Z9q', 'ouyahia_nabil'),
('Bouzidi Djamila', '02/03/1972', 'Alger', 'EPH de Bouira', 'Radiologue', 'k7T3a#W8d', 'bouzidi_djamila'),
('Hamidi Meriem', '08/12/1990', 'Annaba', 'CHU de Batna', 'Pneumologue', 'f2B8n@R6s', 'hamidi_meriem'),
('Hassani Hafid', '16/07/1981', 'Bejaia', 'EPH de Tizi-Ouzou', 'Radiologue', 'd6H2f!Q1w', 'hassani_hafid'),
('Ouldali Amel', '29/11/1988', 'Oran', 'EPH de Sidi Bel Abbes', 'Pneumologue', 'e9C4g%T2y', 'ouldali_amel'),
('Rachidi Samir', '11/05/1975', 'Constantine', 'CHU de Constantine', 'Radiologue', 'b8P3m#V7u', 'rachidi_samir'),
('Boudjemaa Fatima', '03/08/1983', 'Blida', 'EPH de Chlef', 'Pneumologue', 'h3N7s$M2z', 'boudjemaa_fatima'),
('Benali Farid', '20/01/1971', 'Skikda', 'EPH de Biskra', 'Radiologue', 'j9G4x@K2v', 'benali_farid'),
('Rezki Amine', '28/06/1986', 'Tlemcen', 'CHU de Tlemcen', 'Pneumologue', 'g5R6q!H8t', 'rezki_amine'),
('Lounici Ahmed', '09/02/1992', 'El Oued', 'EPH de Ghardaia', 'Radiologue', 'k3T8v#S7p', 'lounici_ahmed'),
('Hakem Nouria', '22/10/1984', 'Boumerdes', 'EPH de Tipaza', 'Pneumologue', 'd7E6y$J9u', 'hakem_nouria'),
('Zerrouki Nadia', '14/01/1976', 'Mostaganem', 'EPH de Saida', 'Radiologue', 'f8R3w#M7z', 'zerrouki_nadia'),
('Belkacem Samia', '27/03/1982', 'Guelma', 'CHU de Bejaia', 'Pneumologue', 'c5U6x@J4h', 'belkacem_samia'),
("Boukharouba Sarah", "02/07/1990", "Oran", "CHU Oran", "Pneumologue", "AzErTy123", "sarah.boukharouba"),
("Kara Djamila", "14/03/1985", "Bejaia", "EPH Bejaia", "Radiologue", "PoIuYtR321", "djamila.kara"),
("Bouzid Omar", "29/11/1992", "Blida", "EPH Blida", "Pneumologue", "MkLoPqN987", "omar.bouzid"),
("Amrouche Samira", "10/09/1988", "Tlemcen", "CHU Tlemcen", "Radiologue", "AsDfGhJ654", "samira.amrouche"),
("Belhadj Yassine", "25/06/1991", "Mascara", "EPH Mascara", "Pneumologue", "QwErTyUi234", "yassine.belhadj"),
("Benali Farida", "07/12/1983", "Constantine", "EPH Constantine", "Radiologue", "PoIuYtR432", "farida.benali"),
("Djelloul Karim", "03/08/1987", "Alger", "CHU Mustapha", "Pneumologue", "MnOpQrSt678", "karim.djelloul"),
("Boudjemaa Khaled", "21/05/1990", "Tizi Ouzou", "EPH Tizi Ouzou", "Radiologue", "ZxCvBnM987", "khaled.boudjemaa"),
("Hamdadou Salima", "17/01/1986", "Annaba", "EPH Annaba", "Pneumologue", "QaWsEdRf765", "salima.hamdadou"),
("Hadjab Mounir", "05/04/1984", "Setif", "EPH Setif", "Radiologue", "YtReWqPo543", "mounir.hadjab"),
]


for l in v:
    NameC, BirthdayC, WilayaC, Hospital, Grade, PasswordC, UsernameC = l
    ClinicianInsert(NameC,BirthdayC, WilayaC,Hospital,Grade,PasswordC, UsernameC)
"""
#ClinicianModify('C000','Bouchama Benamar', '06/04/1978', 'Tipaza', 'CHU de Blida', 'Radiologue', 'f5G5c&3ViXe', 'bouchama_benamar')
ClinicianInsert("Clin24","25/12/1982", 'a','Hospital','Grade','PasswordC', 'user24')
#ClinicianDelete('user24')