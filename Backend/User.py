import Connect_Firebase
import datetime
from MailSending import GenerateMail

db_ref = Connect_Firebase.db.collection('Users')


users = {}
lastid = 0
userIds = []
emails = []


def refresh():
    docs = db_ref.stream()
    global users, userIds, lastid
    userIds = []
    for doc in docs:
        users[doc.id] = doc.to_dict()
        userIds.append(users[doc.id]['UserID'])
        emails.append(users[doc.id]['Email'])
        lastid = int(doc.id.replace("ID", ""))


def check(userID,password):
    refresh()

    for i,j in users.items():
        if '@' in userID:
            if j['Email'] == userID and j['Password'] == password:
                user_doc_id = None
                for doc_id, user_data in users.items():
                    if user_data['Email'] == userID:
                        user_doc_id = doc_id
                        break
                LastLoggedIN = datetime.datetime.now().date()
                LastLoggedIN = datetime.datetime.combine(LastLoggedIN, datetime.datetime.min.time())
                if user_doc_id:
                    try:
                        db_ref.document(user_doc_id).update({"LastLoggedIN": LastLoggedIN})
                        print(f"Password successfully updated for user with email '{userID}'!")
                    except Exception as e:
                        print(f"An error occurred while updating the password: {e}")
                else:
                    print("user not found")
                return True

        else:
            if j['UserID'] == userID and j['Password'] == password:
                user_doc_id = None
                for doc_id, user_data in users.items():
                    if user_data['UserID'] == userID:
                        user_doc_id = doc_id
                        break
                LastLoggedIN = datetime.datetime.now().date()
                LastLoggedIN = datetime.datetime.combine(LastLoggedIN, datetime.datetime.min.time())
                if user_doc_id:
                    try:
                        db_ref.document(user_doc_id).update({"LastLoggedIN": LastLoggedIN})
                        print(f"Password successfully updated for user with email '{userID}'!")
                    except Exception as e:
                        print(f"An error occurred while updating the password: {e}")
                else:
                    print("user not found")
                return True
    return False


def forgotPassword(Email):
    if Email not in emails:
        print("Email does not Exist")
        return "Email does not Exist"
    else:
        print("User Found! Sending OTP")
        GenerateMail(Email)
        return "User Found! Sending OTP"
        

def changePassword(email, newPassword):
    refresh()
    if email not in emails:
        print("Email does not exist")
        return "Email does not exist"

    user_doc_id = None
    for doc_id, user_data in users.items():
        if user_data['Email'] == email:
            user_doc_id = doc_id
            break

    if user_doc_id:
        try:
            db_ref.document(user_doc_id).update({"Password": newPassword})
            print(f"Password successfully updated for user with email '{email}'!")
            return f"Password successfully updated for user with email '{email}'!"
        except Exception as e:
            print(f"An error occurred while updating the password: {e}")
            return f"An error occurred while updating the password: {e}"
    else:
        return "User not found"



def New_User(Username,UserId,Password,Email,Contact,Profile_Pic_url=""):
    
    refresh()
    
    print("Called")
    
    if UserId in userIds:
        return "ID Already Exists"
    if Email in emails:
        return "Email Already Exists"
    
    data_list = {
        "Username":Username,
        "UserID":UserId,
        "Password":Password,
        "Email":Email,
        "Contact":Contact,
        "Points":10,
        "ProfilePic":Profile_Pic_url,
        "is_banned":False,
        }
    
    global lastid
    usermainid = f"ID{lastid+1}"
    lastid +=1
    
    doc_ref = db_ref .document(usermainid)
    
    try:
        doc_ref.set(data_list)
        print(f"Document '{usermainid}' successfully written!")
        return f"Document successfully written!"
    
    except Exception as e:
        return f"An error occurred while writing document '{db_ref}': {e}"
    
refresh()

# New_User("TestUser","TestID","TestPassword","123@asd.asd",123,"asd")