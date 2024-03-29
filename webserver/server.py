
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from datetime import date

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@35.243.220.243/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@35.243.220.243/proj1part2"
#
DATABASEURI = "postgresql://yw3242:0316@35.243.220.243/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  #print(request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT sch_name FROM Previous_School")
  names = []
  for result in cursor:
    names.append(result[0])  # can also be accessed using result[0]
  #print(names)
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("prevschool_index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  return render_template("another.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')











#Fucntion1
@app.route('/prevschool', methods=['POST'])
def prevschool():
    name = request.form['name']
    
    cursor = g.conn.execute("SELECT S.uni FROM Student_Transfer_Advised S Where S.sch_name = %s", name)
    names = []
    for result in cursor:
        names.append(result[0])  # can also be accessed using result[0]
    #print(names)
    cursor.close()
    
    cursor2 = g.conn.execute("SELECT F.prof_name FROM Come_From CF, Faculty F Where CF.sch_name = %s AND F.prof_uni = CF.prof_uni", name)
    #cursor2 = g.conn.execute("SELECT CF.prof_uni FROM Come_From CF Where CF.sch_name = %s", name)
    for result in cursor2:
        names.append(result[0])  # can also be accessed using result[0]
    #print(names)
    cursor2.close()
    

    context = dict(data = names)
    return render_template("findstuprof.html", **context)

#Function2
@app.route('/stuni')
def stuni():
    cursor3 = g.conn.execute("SELECT S.uni FROM Student_Transfer_Advised S")
    uni = []
    for result in cursor3:
        uni.append(result[0])  # can also be accessed using result[0]
    cursor3.close()

    context = dict(data = uni)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
    return render_template("studentuni.html", **context)


@app.route('/stuni_info', methods=['POST'])
def stuni_info():
    
    uni = request.form['name']

    #club
    cursor_club = g.conn.execute("SELECT A.club_name FROM Attend A WHERE A.uni = %s", uni)
    club=[]
    for result in cursor_club:
        club.append(result[0])  # can also be accessed using result[0]
    cursor_club.close()
    
    #research
    cursor_re = g.conn.execute("SELECT EI.proj_name FROM Experience_In EI WHERE EI.uni = %s", uni)
    research=[]
    for result in cursor_re:
        research.append(result[0])  # can also be accessed using result[0]
    cursor_re.close()
    
    #course
    cursor_cour = g.conn.execute("SELECT C.course_name FROM Has_Taken HT, Course_affiliated C WHERE HT.cnumber = C.cnumber AND HT.dept_name = C.dept_name AND HT.uni = %s", uni)
    course=[]
    for result in cursor_cour:
        course.append(result[0])  # can also be accessed using result[0]
    cursor_cour.close()



    context = dict(data1=club,data2=research,data3=course)
  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
    return render_template("studentuni_info.html", **context)


#Function3.1 input club name, return students uni and time
@app.route('/club')
def club():
    cursor = g.conn.execute("SELECT DISTINCT A.club_name FROM Attend A")
    club = []
    for result in cursor:
        club.append(result[0])  # can also be accessed using result[0]
    cursor.close()

    context = dict(data = club)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
    return render_template("club.html", **context)


@app.route('/clubuni', methods=['POST'])
def clubuni():
    

    club = request.form['name']
    info = []

    cursor = g.conn.execute("SELECT DISTINCT A.uni FROM Attend A WHERE A.club_name = %s", club)    
    for result in cursor:
        info.append(result[0])  # can also be accessed using result[0]
    cursor.close()
  

    context = dict(data = info)
  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
    return render_template("clubuni.html", **context)


#Function3.2 input department name, return student uni and course number
@app.route('/course')
def course():
    cursor = g.conn.execute("SELECT DISTINCT T.dept_name FROM Has_Taken T")
    dept = []
    for result in cursor:
        dept.append(result[0])  # can also be accessed using result[0]
    cursor.close()

    context = dict(data = dept)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
    return render_template("course.html", **context)


@app.route('/courseuni', methods=['POST'])
def courseuni():
    

    dept = request.form['name']
    info = []

    cursor = g.conn.execute("SELECT T.cnumber, T.uni FROM Has_Taken T WHERE T.dept_name = %s", dept)    
    for result in cursor:
        info.append(result)  # can also be accessed using result[0]
    cursor.close()
  

    context = dict(data = info)
  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
    return render_template("courseuni.html", **context)

#Function4 Input research name, output supervisor uni and student uni
@app.route('/research')
def research():
    cursor = g.conn.execute("SELECT DISTINCT E.proj_name FROM Experience_in E")
    research = []
    for result in cursor:
        research.append(result[0])  # can also be accessed using result[0]
    cursor.close()

    context = dict(data = research)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
    return render_template("research.html", **context)

@app.route('/researchuni', methods=['POST'])
def researchuni():
  

    dept = request.form['name']
    info = []

    cursor = g.conn.execute("SELECT F.prof_name,E.uni FROM Experience_in E, Supervise S, Faculty F WHERE E.proj_name = S.proj_name AND S.proj_name = %s AND F.prof_uni=S.prof_uni", dept)    
    for result in cursor:
        info.append(result)  # can also be accessed using result[0]
    cursor.close()
  

    context = dict(data = info)
  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
    return render_template("researchuni.html", **context)

#Function5 Input department name, output name of professor who advised transfers before and their research fields
@app.route('/prof')
def prof():
    cursor = g.conn.execute("SELECT DISTINCT W.dept_name FROM Work_in W")
    prof = []
    for result in cursor:
        prof.append(result[0])  # can also be accessed using result[0]
    cursor.close()

    context = dict(data = prof)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
    return render_template("prof.html", **context)

@app.route('/profinfo', methods=['POST'])
def profinfo():

    dept = request.form['name']
    info = []

    cursor = g.conn.execute("SELECT F.prof_name, F.research_field FROM Faculty F, Work_in W WHERE W.dept_name = %s AND F.prof_uni=W.prof_uni", dept)    
    for result in cursor:
        info.append(result)  # can also be accessed using result[0]
    cursor.close()
  

    context = dict(data = info)
  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
    return render_template("profinfo.html", **context)

#Function6 store new club-uni dataset into Attend table
@app.route('/attend')
def attend():

    cursor = g.conn.execute("SELECT S.uni FROM Student_Transfer_Advised S")
    cursor2 = g.conn.execute("SELECT DISTINCT A.club_name FROM Attend A")
    stu = []
    club=[]
    for result in cursor:
        stu.append(result[0])  # can also be accessed using result[0]
    cursor.close()

    for result in cursor2:
        club.append(result[0])  # can also be accessed using result[0]
    cursor2.close()

    context = dict(data1=stu,data2=club)

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
    return render_template("attend.html", **context)

@app.route('/insert', methods=['POST'])
def insert():
  
    uni = request.form['uni']
    club = request.form['club']
    inserted=0
    cursor = g.conn.execute("SELECT A.club_name FROM Attend A WHERE A.uni=%s",uni)
    clubs=[]
    for result in cursor:
        clubs.append(result[0])  # can also be accessed using result[0]
    cursor.close()

    if club not in clubs:
        today = date.today()
        engine.execute("INSERT INTO Attend (uni, club_name, start_time) VALUES (%s,%s,%s)",uni,club,today)
        inserted=1
    
    context = dict(data=[inserted,inserted])
  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
    return render_template("insert.html", **context)


    
@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
