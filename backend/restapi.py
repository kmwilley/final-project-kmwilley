import flask

from flask import jsonify
from flask import request

from sql import DBconnection
from sql import execute_read_query
from sql import execute_update_query

import creds

#setup an application
app = flask.Flask(__name__)
app.config['DEBUG'] = True

# General API to call home page request with GET method
@app.route('/', methods=['GET'])
def home():
    return "<h1> Hello, Welcome to 2368 class </h1>"

# In-memory student list with two students information
students = [
    {
        "id":100,
        "fname": "suresh",
        "lname": "peddoju"
    },
    {
        "id":101,
        "fname": "suresh2",
        "lname": "peddoju2"
    }
]

# API to retrive all students information from in-memory student list using request [GET] method
@app.route('/students/all', methods=['GET'])
def allstudents():
    return jsonify(students)

# API to retrive single student information from in-memory student list using request [GET] method
@app.route('/students/single', methods=['GET'])
def singlestudent():
    # request.args consists of parameter arguments passed in request. 
    # Below code retriving parameter 'id' from request arguments 
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No ID found"

    for student in students:
        if student['id']==id:
            return(student)
        
# API to update in memory student list [POST] method
@app.route('/students/update', methods=['POST'])
def updatestudent():
    userinput = request.get_json() # Pass new user info in JSON format within Body of the request

    newid = userinput['id']
    newfname = userinput['fname']
    newlname = userinput['lname']

    students.append({"id": newid, "fname": newfname, "lname": newlname})
    print("A new students record inserted")
    return "A new student is added"

# The following code shows Database access with REST API's using GET, POST, PUT and DELETE methods

# API requst for retriving all users information from DB with GET method
@app.route('/users/all', methods=['GET'])
def allusers():
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)

    sql = "select * from users"

    userrows = execute_read_query(mycon, sql)
    return jsonify(userrows)

# API requst for retriving single users information from DB with GET method by passing 'id' as argument parameters
@app.route('/users/single', methods=['GET'])
def singleuser():
    # request.args consists of parameter arguments passed in request. 
    # Below code retriving parameter 'id' from request arguments 
    if 'id' in request.args:    
        id = int(request.args['id'])
    else:
        return 'Error: No ID is provided!'
    
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = "select * from users"
    userrows = execute_read_query(mycon, sql)
    results = []

    for user in userrows:
        if user['id']== id:
            results.append(user)
    return jsonify(results)

#API request to Insert a new user to DB with POST method
@app.route('/users/insertnewuser', methods=['POST'])
def insertnewuser():
    userinput = request.get_json() # Pass new user info in JSON format within Body of the request
    newfname = userinput['fname']
    newlname = userinput['lname']
    newemail = userinput['email']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = "insert into users(fname, lname, email) values ('%s','%s','%s')" % (newfname, newlname, newemail)

    execute_update_query(mycon, sql)
    return 'Add user request successful!'

# Delete a user with DELETE method
@app.route('/users/deleteuser', methods=['DELETE'])
def api_delete_user_byID():
    userinput = request.get_json() # Pass user ID in JSON format within Body of the request
    idtodelete = userinput['id']
    
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = "delete from users where id = %s" % (idtodelete)
    execute_update_query(mycon, sql)
        
    return "Delete request successful!"

# Update user information using request PUT method
@app.route('/users/updateuser', methods=['PUT'])
def updateuser():
    userinput = request.get_json() # Pass user ID and email in JSON format within Body of the request
    id = userinput['id']
    newemail = userinput['email']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = "update users set email='%s' where id='%s'" % (newemail, id)

    execute_update_query(mycon, sql)
    return 'User update successful!'

app.run()

