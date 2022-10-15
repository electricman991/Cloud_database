# Overview

This program interfaces with the Google Firestore database and allows data to be pulled about workers in a company. This information is accesssed by the user through a console interface that can be used to insert, modify, delete or retrieve data. The user selects a number to interact with the database and depending on what they choose can modify data for workers within the database. 

I wrote this software to better understand how to interact with cloud databases and how I could implement a cloud database with other projects that I will be working on. 

[Software Demo Video](https://youtu.be/zGP4TS6cuiw)

# Cloud Database

Google Firestore

There is a collection that contains all the workers with each person's name being a document for information that is related such as a salary or address information. 

# Development Environment

Visual Studio Code

Python 3.9.5
Firebase_admin

# Useful Websites

* [Google Cloud](https://cloud.google.com/firestore/docs/create-database-server-client-library#windows)

# Future Work

* Implement user authentication 
* Receive notifications for when data is updated
* Add more fields for user data