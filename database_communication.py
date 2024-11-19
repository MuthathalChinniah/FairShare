
# https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/
# https://www.mongodb.com/try/download/community
import pymongo
import re


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["FairShare_DB"] #Creating Database with the name FairShare_DB
user_login_details = mydb["UserDetails"] #Creating a Collection for user login details


def validate_mobile (mobile):
    """
    Validates a mobile number: only numbers, 10 digits
    :param mobile: str mobile number to validate
    :return: bool: true/ false: valid/ invalid
    """
    pattern = r"\d{10}$"
    return bool(re.match(pattern, mobile))

def mobile_exists(mobile):
    """
    To check if a mobile number exists already
    :param mobile: str mobile number
    :return: bool: True: already exists, False: does npt exist
    """
    query = {"Mobile": mobile}
    return bool(user_login_details.find_one(query))



def validate_email(email):
    """
    Validates an email address
    Rules:  any alpha num or some special char, followed by @, followed by alpha num, followed by . , followed by at least two letter alpha
    :param: email (str): The email address to validate.
    :return: bool: True if valid, False otherwise.
    """
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return (re.match(email_pattern, email))

def validate_password(password):
    """
        1. At least one capital letter
        2. At least one small letter
        3. At least one number
        4. At least 8 characters total
    :param password: str
    :return: bool: true: valid, false: invalid
    """
    password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$"
    return bool(re.match(password_pattern, password))

def create_user_db (name, mobile, password, email=None):
    """
    Create user in UserLogin connection
    :param name: str: Name of user
    :param mobile: str: mobile of user
    :param password: str
    :param email: str
    :return: bool: created successfully or not
    """
    if not validate_mobile(mobile):
        print("Mobile number invalid")
        return False
    if mobile_exists(mobile):
        print("This Mobile number number already has an account")
        return False
    if len(name) < 1:
        print("Enter a valid Name")
        return False
    if email is not None:
        if not validate_email(email):
            print("Invalid email id")
            return False
    if not validate_password(password):
        print("""Invalid Password: Password should contain:
        1. At least one capital letter
        2. At least one small letter
        3. At least one number
        4. At least 8 characters total""")
        return False
    this_user = {"Name": name, "Mobile": mobile, "Password": password, "Email": email}
    user_login_details.insert_one(this_user)
    print("Created")
    return True


def login(mobile, password):
    """
    To login to an existing user acc
    :param mobile: str: mobile number
    :param password: str
    :return: bool: logged in successfully or not
    """
    query = {"Mobile": mobile}
    doc = user_login_details.find_one(query)
    if bool(doc):
        if doc['Password'] == password:
            print("Logged in")
            return True
        else:
            print("Invalid Password")
            return False
    else:
        print("Invalid mobile number")
        return False


create_user_db("Kirti Mohan", "1234867891", "P@skw0rd1")
login("1234867891", "P@skw0rd1")

