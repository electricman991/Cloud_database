import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def initialize_firestore():
    """
    Create database connection
    """

    # Setup Google Cloud Key File
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = "cloud_database/data-storage-1d253-firebase-adminsdk-f4xz9-b1a1a85bae.json"

    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'data-storage-1d253',
    })

    # Get reference to database
    db = firestore.client()
    return db

def add_new_employee(db):
    '''
    Prompt the user for a new worker that will be added to the database.  
    '''

    name = input("Full Name: ")
    address = (input("Address: "))
    salary = float(input("Salary: "))

    # Check for an already existing worker by the same name.

    result = db.collection("workers").document(name).get()
    if result.exists:
        print("Item already exists.")
        return

    # Build a dictionary to hold the contents of the firestore document.
    data = {"address" : address, 
            "salary" : salary}
    db.collection("workers").document(name).set(data) 

    # Save this in the log collection in Firestore       
    log_transaction(db, f"Added {name}")

def delete_worker(db):
    '''
    Prompt the user to delete a worker from the database.  
    '''

    name = input("Worker Name: ")

    # Check for an already existing item by the same name.
    # The document ID must be unique in Firestore.
    result = db.collection("workers").document(name).get()
    if not result.exists:
        print("Invalid Item Name")
        return

    # Delete the item from the database
    
    db.collection("workers").document(name).delete()

    # Save this in the log collection in Firestore
    log_transaction(db, f"Deleted {name}")

def update_info(db):
    '''
    Prompt the user to use quantity from an already existing item in the
    inventory database.  An error will be given if the requested amount
    exceeds the quanity in the database.
    '''

    print("Only update the information you want to change\n")
    name = input("Worker Name: ")
    print("If salary is not changing, enter 0")
    new_salary = float(input("New Salary: "))
    print("If address is not changing, click enter")
    new_address = input("New Address: ")

    # Check for an already existing item by the same name.
    # The document ID must be unique in Firestore.
    result = db.collection("workers").document(name).get()
    if not result.exists:
        print("Invalid Name")
        return

    # Convert data read from the firestore document to a dictionary
    data = result.to_dict()

    # Update the dictionary with the new data and then save the 
    # updated dictionary to Firestore.
    if new_address == '' and new_salary == 0:
        pass
    
    elif new_salary > 0:
        data["salary"] = new_salary
        db.collection("workers").document(name).set(data)
    elif new_address != '':
        data["address"] = new_address
        db.collection("workers").document(name).set(data)

    # Save this in the log collection in Firestore
    log_transaction(db, f"Updated {name}'s information ")

def search_workers(db):
    '''
    Search the database in multiple ways.
    '''

    print("Select Query")
    print("1) Show All workers")        
    print("2) Show All workers Salaries")
    choice = input("> ")
    print()

    # Build and execute the query based on the request made
    if choice == "1":
        results = db.collection("workers").get()
        print("")
        print("Search Results")
        print(f"{'Name':<20}  {'Address':<10}  {'Salary':<10}")
        for result in results:
            item = result.to_dict()
            print(f"{result.id:<20}  {item['address']:<10}  {item['salary']:<10}")
        print()    
    elif choice == "2":
        results = db.collection("workers").get()
        print("")
        print("Search Results")
        print(f"{'Name':<20}  {'Salary':<10}")
        for result in results:
            item = result.to_dict()
            print(f"{result.id:<20} {item['salary']:<10}")
        print()    
    else:
        print("Invalid Selection")
        return
    
    # Display all the results from any of the queries
    

def log_transaction(db, message):
    '''
    Save a message with current timestamp to the log collection in the
    Firestore database.
    '''
    data = {"message" : message, "timestamp" : firestore.SERVER_TIMESTAMP}
    db.collection("log").add(data)    


def main():
    db = initialize_firestore()
    choice = None
    while choice != "0":
        print()
        print("0) Exit")
        print("1) Add New Worker")
        print("2) Delete Worker")
        print("3) Update Salary")
        print("4) Search Workers")
        choice = input(f"> ")
        print()
        if choice == "1":
            add_new_employee(db)
        elif choice == "2":
           delete_worker(db)
        elif choice == "3":
           update_info(db)
        elif choice == "4":
            search_workers(db)                        

if __name__ == "__main__":
    main()
