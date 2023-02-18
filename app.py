#!/usr/bin/env python
# coding: utf-8

# In[3]:


from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def base():
    return render_template('base.html')



@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        message, handle = insert_message(request)
        return render_template('submit.html', epilogue = True, message = message, handle = handle)



@app.route('/view/')
def view():
    messages = random_messages(3)
    return render_template('view.html', messages = messages)
    

        
def get_message_db():
    '''
    Check is there exits a table named messages in message_db or not.
    If there is a database called message_db in the g attribute of the app,using the try except command to test .
    If there is, just return the database. 
    if there is not, go to the except.
    '''
    
    
    try:
        return g.message_db
    
    
    # If there is no database in g, we need connect one in the attribute g
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        
        
        # Using SQL command to check if there is a table named messages in messages_db.
        # If there is no table exit, just create one with three columns: id, handle, and message.
        cmd = """CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                handle TEXT,
                message TEXT)"""
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db
    
    
def insert_message(request):
    
    # Extracting message and handle.
    message = request.form['message']
    handle = request.form['handle']
    
    # Call get_message_db() to connect to the database.
    db = get_message_db()
    
    # Creating a cursor object.
    cursor = db.cursor()
    
    # Finding current number of row of the table. 
    cursor.execute("SELECT COUNT(*) FROM messages")
    id_num = cursor.fetchone()[0] + 1
    
    # Insert id, message, and handle into the table.
    cursor.execute("INSERT INTO messages (id, handle, message) VALUES (?, ?, ?)", (id_num, handle, message))
    db.commit()
    
    # Close connection
    db.close()
    
    return message, handle


def random_messages(n):
    
    # Call get_message_db() to connect to the database.
    db = get_message_db()
    
    # Creating a cursor object.
    cursor = db.cursor()
    
    # Choosing n random messages from the table.
    cursor.execute("SELECT * FROM messages ORDER BY RANDOM() LIMIT ?",(n,))
    
    # Output all the messages.
    messages = cursor.fetchall()
    
    # close the connection.
    db.close()
    
    return messages


# In[ ]:




