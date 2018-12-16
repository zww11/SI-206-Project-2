# ZeyaoWang
# Final Project
# link of Github: https://github.com/SI206-UMich/final-project-zww11
import sys
import email, getpass, imaplib, os, re
import matplotlib.pyplot as plt
import sqlite3
import json
import csv

# Get Gmail user name and passwords
user = input("Enter your Gmail username --> ")
pwd = getpass.getpass("Enter your password --> ")
imap_url = 'imap.gmail.com'
detach_dir = "/Users/apple/Desktop/final-project-zww11"

# PART 1 - Get Data
# Access the API for a social media site or website of your choice 
# (e.g., Facebook, GitHub, Instagram, Gmail, YouTube or any other site you have an active account with).
# Cache the data in a SQLite database over time (must have a way to check if the data is already in the database, 
# the ability to be restarted, and must limit how much data it collects at a time).
# Access and store in the database at least 100 interactions (posts, emails, commits, likes, etc) using the API.

# Set up the Auth
def auth(user, pwd, imap_url):
    con = imaplib.IMAP4_SSL(imap_url)
    try:
        con.login(user, pwd)
    except imaplib.IMAP4.error:
        print("Login Failed!")
        sys.exit()
    return con

# Extracts emails from different Sender
def get_specificEmail(emailAddress):
    temp_command = '(FROM "' + emailAddress + '")'
    resp, items = con.search(None, temp_command)
    items = items[0].split()
    print(len(items))
    break_ = False
    
    final_list = []
    
    for emailid in items:
        if ( break_ ):
            break
        temp_dict = {}
        resp, data = con.fetch(emailid, "(RFC822)")
        email_body = data[0][1]
        msg = email.message_from_bytes(email_body)
        temp_dict['Sender'] = msg["from"]
        temp_dict['Receiver'] = msg["to"]
        temp_dict['Subject'] = msg["subject"]
        temp_dict['DateOfSend'] = msg["date"]
        final_list.append(temp_dict)
    # print(final_list)
    return final_list


# Login in an account
con = auth(user, pwd, imap_url)
con.select('INBOX')
con.list()

# Set up Database Email_Data_SQL.sqlite3
conn = sqlite3.connect('ZeyaoWang-Part1_Email_Data_SQL.sqlite3')
cur = conn.cursor()

# Create Email Table
cur.execute('DROP TABLE IF EXISTS Email')
cur.execute('CREATE TABLE Email (Sender TEXT, Receiver TEXT, Subject TEXT, DataOfSend TIMESTAMP)')

# Ask for specific email address and Store data in the json file
filename = open('ZeyaoWang-Part1_Email_Data.json', 'w')
jsonData = json.dumps(get_specificEmail(input("Enter the specific sender's email address you want to search --> ")), indent=2)
filename.write(jsonData)
filename.close()

# Read the cache from the file if it exists
try:
    file = open('ZeyaoWang-Part1_Email_Data.json', 'r')
    contents = file.read()
    dic = json.loads(contents)
    file.close()
except:
    print("Error when reading from file")
    dic = {}

# Use a for loop to insert data
for da in dic:
    data = da['Sender'], da['Receiver'], da['Subject'], da["DateOfSend"]
    cur.execute('INSERT INTO Email (Sender, Receiver, Subject, DataOfSend) VALUES (?, ?, ?, ?)', data)

conn.commit()


# PART 2 - Process Dsata
# Calculate something from the data such as the number of items (posts, likes, etc) per day (Sunday, Monday, etc), 
# the day with the most items, the day with the least items, and the average number of items per day.
# Create a “report” - (screen display, file output, or other easy-to-read formats) that contains the calculated data. 
# The report can be terminal output or a .json/.csv/.txt file that is easy to read

# Calculate the email received each day of the week
def getDayDict(cur):
    cur.execute('SELECT DataOfSend FROM Email')
    result = cur.fetchall()
    result2 = {'Sun':0, 'Mon':0, 'Tue':0, 'Wed':0, 'Thu':0, 'Fri':0, 'Sat':0, }
    for i in result:
        weekday = i[0][0:3]
        if weekday == 'Sun':
            result2['Sun'] += 1
        elif weekday == 'Mon':
            result2['Mon'] += 1
        elif weekday == 'Tue':
            result2['Tue'] += 1
        elif weekday == 'Wed':
            result2['Wed'] += 1
        elif weekday == 'Thu':
            result2['Thu'] += 1
        elif weekday == 'Fri':
            result2['Fri'] += 1
        elif weekday == 'Sat':
            result2['Sat'] += 1
    return result2

# Export data to csv file
def dictTocsv(diction):
    with open('ZeyaoWang-Part2_Report.csv','w') as f:
        w=csv.writer(f)
        w.writerow(diction.keys())
        w.writerow(diction.values())

dictTocsv(getDayDict(cur))

# PART 3 - Plot Data
# Suggestions of visualizations include comparing social media accesses on each day of the week, 
# a google map with the locations of your Facebook friends, a Word Cloud, etc.

# Draw a Bar Chart to show how much emails received each day of the week
def drawBarChart(dayDict):
    names = dayDict.keys()
    values = dayDict.values()

    plt.bar(names, values, facecolor='orange')
    plt.title('The Number of Emails Received Each Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Emails')
    plt.savefig("ZeyaoWang-Part3_Bar.png")
    plt.show()

drawBarChart(getDayDict(cur))










