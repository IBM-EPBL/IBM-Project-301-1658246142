from flask import Flask, render_template, request, url_for, redirect
import ibm_db

app = Flask(__name__)

def db2_conn():
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=E:\IBM\DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=yzj33829;PWD=eBVQ0wHevWV7Rhx5;",'','')
    return conn

@app.route("/")
def index():
    return render_template('register.html')

@app.route("/register",methods = ['POST'])
def register():
    if request.method == 'POST':
        conn = db2_conn()
        insert_sql = "INSERT INTO USER (EMAIL,USERNAME,ROLLNO,PASSWORD) VALUES ('{0}','{1}',{2},'{3}')".format(request.form['email'],request.form['uname'],request.form['rollno'],request.form['pass'])
        print(insert_sql)
        ibm_db.exec_immediate(conn,insert_sql)
        ibm_db.close(conn)
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        conn = db2_conn()
        stmt = "SELECT USERNAME FROM USER WHERE USERNAME = '{0}' AND PASSWORD = '{1}'".format(request.form['uname'],request.form['pass'])
        res = ibm_db.exec_immediate(conn,stmt)
        rc = ibm_db.fetch_assoc(res)
        ibm_db.close(conn)
        if rc:
            return render_template('welcome.html',username=request.form['uname'])
        else:
            return render_template('login.html', error="Invalid Username/Password")
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)