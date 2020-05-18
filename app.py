from flask import Flask , render_template , request , redirect , url_for
import sqlite3
import os




app = Flask(__name__)

email_curr = ""
@app.route("/Profile" , methods=["GET","POST"])
def upload_files():
    if request.method=="POST":
        files = request.files.getlist("file")
        #-----------------REMOVING EXISTING FILES FROM TEST----------------------------------
        files_database = os.listdir("TEST")
        if(len(files_database)>0):
            for file in files_database:
                path = os.path.join("TEST",file)
                os.remove(path)
        #---------------------------------------------------------------------------------------

        for file in files:
            file.save(os.path.join("TEST", file.filename))
        os.system("predict.py")
        return render_template("PROFILE.html",list_email=email_curr)

    return render_template("PROFILE.html",list_email=email_curr)
    



@app.route("/Login",methods=['GET', 'POST'])
def LOGIN(): 
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("psw")
        conn = sqlite3.connect("database.db", check_same_thread=False)
        c1 = conn.cursor()
        c1.execute("SELECT * FROM USERS where EMAIL=? AND PASSWORD=? ",(email,password))
        data_tab = c1.fetchall()
        if(len(data_tab)==0):
            conn.close()
            data = ["Sorry NO User Found :(  Please Register First ..!"]
            return render_template("LOGIN.html",list_to_send=data)
        else:
            conn.close()
            msg = "User:- "+email
            email_curr = msg
            return redirect(url_for("upload_files"))
            
    return render_template("LOGIN.html")

@app.route("/Register",methods=['GET', 'POST'])
def REGISTER():
    if request.method == 'POST':
        email1 = request.form.get("u_email")
        password1 = request.form.get("u_pass")
        conn = sqlite3.connect("database.db", check_same_thread=False)
        c1 = conn.cursor()
        c1.execute("SELECT * FROM USERS where EMAIL=?",(email1,))
        data_tab = c1.fetchall()
        if(len(data_tab)==0):
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS USERS( EMAIL VARCHAR(30) , PASSWORD VARCHAR(20) )")
            c.execute("INSERT INTO USERS (EMAIL , PASSWORD) VALUES (? , ?)",( email1,password1))
            print("SUCCESS")
            conn.commit()
            conn.close()
            return redirect("/Login")
        else:
            conn.close()
            data =["USER already present :("]
            return render_template("REGISTER.html",list_to_send=data)
        
        
        
    return render_template("REGISTER.html")


if __name__ == "__main__":
    app.run(debug=True)