# https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/
# https://www.mongodb.com/try/download/community
import pymongo
from bson.objectid import ObjectId
from numbers import Number



myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#myclient.drop_database("FairShare_DB") #To drop the whole database and start afresh
mydb = myclient["FairShare_DB"] #Creating Database with the name FairShare_DB

user_login_details = mydb["UserDetails"] #Each doc is of format: {"Name": name, "Mobile": mobile, "Password": password, "Email": email}
friends = mydb ["Friends"] #Each doc is of format: {"user_id": user_id, "Friend": str_friend's_user_id}
group_names = mydb["GroupNames"] #Each doc is of format: {"group_name": group_name, "_id": str}
group_members = mydb["GroupMem"] #Each doc is of format: {"group_id": str, "user_id": str}
group_expenses = mydb["Expenses"] #Each doc is of format: {"group_id": group_id, "amount": float, "description": Description_str}
expenses_split = mydb ["ExpensesSplit"] #Each doc is of format: {"user_id": str, "split": float (amount split for this person)}
payments = mydb ["Payments"]#Each doc is of format: {"from": user id, "to": user_id, "amount": float (amount split if group payment or full amount if settle up)}



def mobile_exists(mobile):
    """
    Created by Muthathal
    To check if a mobile number exists already
    :param mobile: str mobile number
    :return: bool: True: already exists, False: does npt exist
    """
    query = {"Mobile": mobile}
    return bool(user_login_details.find_one(query))


def create_user_db (name, mobile, password, email=None):
    """
    Create user in UserLogin connection
    :param name: str: Name of user
    :param mobile: str: mobile of user
    :param password: str
    :param email: str
    :return: bool: created successfully or not, str: staus/ reason
    """
    if mobile_exists(mobile):
        message = "This Mobile number number already has an account"
        return False, message


    this_user = {"Name": name, "Mobile": mobile, "Password": password, "Email": email}
    user_login_details.insert_one(this_user)
    message = "Created"
    return True, message


def login(mobile, password):
    """
    Created by Muthathal
    To login to an existing user acc
    :param mobile: str: mobile number
    :param password: str
    :return: bool: logged in successfully or not, str: status/ reason
    """
    query = {"Mobile": mobile}
    doc = user_login_details.find_one(query)
    if bool(doc):
        if doc['Password'] == password:
            message = str(doc['_id'])
            return True, message
        else:
            message = "Invalid Password"
            return False, message
    else:
        message = "No account exists with this mobile number"
        return False, message







def get_acc_details (user_id):
    """
    To get details of the current user account
    :param: user_id
    :return: dict: Dictionary containing all the account details
    """
    pass #SR

def add_friend (user_id, mobile_number_of_friend):
    """
    To add a friend to my friends list: Requires: Valid Mobile number, valid user_id, Not already a friend.
    Else returns False with the appropriate error message
    :param user_id: str
    :param mobile_number_of_friend: str
    :return: bool-status, str-message
    """
    query = {"Mobile": mobile_number_of_friend}
    doc = user_login_details.find_one(query)
    if bool(doc):
        if user_exists(user_id):
            if doc['Name'] not in get_friends(user_id):
                friend = {"user_id": user_id, "Friend": str(doc['_id'])}
                friends.insert_one(friend)
                return True, "Success"
            else:
                return False, "This Person is already your friend"
        else:
            return False, "Invalid User"
    else:
        return False, "No account exists with this mobile number"


def user_exists (user_id):
    """
    To check if user id given is a valid one-Internal usage for backend
    :param user_id: str
    :return: bool: valid/invalid
    """
    query = {"_id": ObjectId(user_id)}
    doc = user_login_details.find_one(query)
    return bool(doc)

def get_activity ():
    pass #SR
    #Can be implemented later if time permits




def create_group (user_id, group_name, friends_list):
    """
    Create a group: requirements: All friends' user id in friends_list must be valid, current user id must be valid, group name must have at least 1 character
    :param user_id: str
    :param group_name: str
    :param friends_list: list of str of friends' ids
    :return: bool: created/not created,   message: str: If created: group_id, else: error message
    """
    if user_exists(user_id):
        if len(group_name) > 0:
            group_id = group_names.insert_one({"group_name": group_name})
            group_id = str(group_id.inserted_id)
            for friend in friends_list:
                if user_exists(friend):
                    group_members.insert_one({"group_id": group_id, "user_id": friend})
                else:
                    return False, "Invalid friend"
            group_members.insert_one({"group_id": group_id, "user_id": user_id})
            return True, "Created group"
        else:
            return False, "Invalid group name"
    else:
        return False, "Invalid User"


def group_exists (group_id):
    """
    To check if group id given is a valid one-Internal usage for backend
    :param group_id: str
    :return: bool: valid/invalid
    """
    query = {"_id": ObjectId(group_id)}
    doc = group_names.find_one(query)
    return bool(doc)


def add_friend_to_group (group_id, friend_id):
    """
    Add friend to an existing group
    :param group_id: str
    :param friend_id: str
    :return: Bool: status, message: str
    """
    if user_exists(friend_id):
        if group_exists(group_id):
            members = get_group_members(group_id)
            if friend_id not in members.values():
                group_members.insert_one({"group_id": group_id, "user_id": friend_id})
                return True, "Success"
            else:
                return False, "This person is already a member of this group"
        else:
            return False, "Invalid Group"
    else:
        return False, "Friend Invalid"


def add_group_expense_split (amount, user_list, paid_by):
    """
    Internal function to add expenses and payment split for each person in the list of users provided
    Default split is: Split Equally
    Expense: {"user_id": str, "split": float (amount split for this person)}
    Payment: {"from": user id, "to": user_id, "amount": float (amount split if group payment or full amount if settle up)}
    :param amount: float
    :param user_list: list of str: list of user_ids
    :return: None
    """
    amount_share = amount/len(user_list)
    for user_id in user_list:
        if user_id != paid_by:
            payments.insert_one({"from": paid_by, "to": user_id, "amount": amount_share})
        expenses_split.insert_one({"user_id": user_id, "split": amount_share})

def add_group_expense (paid_by, group_id, amount, description):
    """
    Add expense to group: {"group_id": group_id, "amount": float, "description": Description_str}
    :param paid_by: str (user id)
    :param group_id: str
    :param amount: float
    :param description: str: comment about the expense
    :return: bool: status, message: Success/ Error message
    """
    if user_exists(paid_by):
        if group_exists(group_id):
            if isinstance(amount, Number):
                amount = float(amount)
                if amount > 0:
                    this_expense = {"group_id": group_id, "amount": amount, "description": description}
                    group_expenses.insert_one(this_expense)
                    all_members = (get_group_members(group_id)).values ()
                    if len(all_members)>0:
                        add_group_expense_split (amount, all_members, paid_by)
                        return True, "Success"
                    else:
                        return False, "Add at least one member to the group before adding expense"
                else:
                    return False, "Enter a value greater than 0 for amount"
            else:
                return False, "Enter a numeric value for amount"
        else:
            return False, "Invalid Group"
    else:
        return False, "Enter a valid user for Paid By"




def settle_up (user_id, group_id, paid_by, paid_to, amount):
    """
    To settle up any balances in a group
    :param user_id: str
    :param group_id: str
    :param paid_by: str: id of person paying
    :param paid_to: str: id of person receiving
    :param amount: float
    :return: message: str
    """
    pass  # SA

def get_balances (user_id, group_id):
    """
    Get balances of the current group
    :param user_id: str
    :param group_id: str
    :return: dict: dictionary containing all the balance details
    """
    pass  # SA

def all_groups (user_id):
    """
    Return all groups of a given user (if given user id is valid)
    :param user_id: str
    :return: bool: valid or invalid user, dictionary of format: {group_name1: group1_id, group_name2: group2_id, ...}
    """
    if user_exists(user_id):
        query = {"user_id": user_id}
        cursor = group_members.find(query)
        group_dict = {}
        for group in cursor:
            g_id = group['group_id']
            group_name = group_names.find_one({"_id": ObjectId(g_id)})
            group_name = group_name["group_name"]
            group_dict [group_name] = g_id
        return True, group_dict
    else:
        return False, {}



def get_friends(user_id):
    """
    Get all friends names and ids of current user
    :param: user_id: str
    :return: dictionary {friend_name_1: friend_id_1, friend_name_2: friend_id_2, ....}
    """
    cursor = friends.find({"user_id": user_id})
    friends_dict = {}
    for doc in cursor:
        user_details = user_login_details.find_one({"_id": ObjectId(doc['Friend'])})
        friends_dict [user_details['Name']] = str(user_details["_id"])
    return friends_dict



def get_group_members (group_id):
    """
    Get all members of given group and their corresponding id
    :param group_id: str
    :return: dictionary {member_name_1: member_id_1, member_name_2: member_id_2, ....}
    """
    cursor = group_members.find({"group_id": group_id})
    friends_dict = {}
    for doc in cursor:
        user_details = user_login_details.find_one({"_id": ObjectId(doc['user_id'])})
        friends_dict[user_details['Name']] = str(user_details["_id"])
    return friends_dict













def my_tester():
    """Testing function- only for internal usage- testing"""

    # testing Create user, login
    print(create_user_db("Kirti Mohan", "1234867891", "P@skw0rd1"))
    print(login("1234867891", "P@skw0rd1"))

    #Creating a user
    print(create_user_db("Jana","0154982398", "Pass@123", None))

    #Finding a doc with ID
    cursor = user_login_details.find({})
    for doc in cursor:
        print(doc)
    doc = user_login_details.find_one({"_id": ObjectId(str("6750cb6f89b3bae87530d7d7"))})
    print(doc['Name'], "<><><><>")


    #Adding friend for a user
    print (add_friend("6750cb6f89b3bae87530d7d7", "6666666660"))


    #Creating group
    #print (create_group("6750cb6f89b3bae87530d7d7", "MyGroup2", ["67587f0aacf79394c68b9e2d", "67587f6ffd9b042fc40967b4"]))
    cursor = group_names.find({})
    for doc in cursor:
        print(doc)


    #Getting all groups of one user
    print("Groups of Janu: ", all_groups("67587f0aacf79394c68b9e2d"))
    print("Groups of Jana: ", all_groups("67587f6ffd9b042fc40967b4"))
    print("Groups of Muthu: ", all_groups("6750cb6f89b3bae87530d7d7"))
    print("Groups of M: ", all_groups("67422a0e996fe564d452c286"))

    print(add_friend_to_group("67589aea0b4491008ed0ce28", "6740be446182fd93bf472312"))

    #Adding a group expense
    #print(add_group_expense ("67587f6ffd9b042fc40967b4", "67589bc4ba6cf3fe9ac35863", 30, "Groceries"))
    print("Group Expenses <><><><><><><><><><><><><><><><><><>")
    cursor = group_expenses.find({})
    for doc in cursor:
        print(doc)

    print("Expenses Split <><><><><><><><><><><><><><><><><><>")
    cursor = expenses_split.find({})
    for doc in cursor:
        print(doc)

    print("Payments split <><><><><><><><><><><><><><><><><><>")
    cursor = payments.find({})
    for doc in cursor:
        print(doc)
if __name__ == "__main__":

    my_tester()

