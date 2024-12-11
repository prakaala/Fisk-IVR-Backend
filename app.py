from datetime import datetime
from flask import Flask, render_template, request
import random
from mysql.connector import connect, Error
app = Flask(__name__)

@app.route("/")
def firstApp():
    return render_template("home.html")

@app.route('/form', methods=['GET'] )
def render_form():
    return render_template('form.html')

@app.route('/scholarship', methods=['GET'])
def render_scholarship():
    return render_template('scholarship.html')


@app.route('/saveScholarship', methods= ['POST'])
def scholarship():
    print(request.form)
    first = request.form.get('fName')
    scholarship = request.form.get('scholarshipAmount')
    userName = request.form.get('userName')
    studentID = request.form.get('studentID')
    try:
        if studentID is None or scholarship is None:
            raise ValueError("Missing required parameters: 'student_id' or 'amount'")
        with connect(
host = "",
user = "",
password = "",
 database = ""

        ) as connection:
            print(connection)
            query = "UPDATE scholarship SET amount = %s WHERE student_id = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (scholarship, studentID))
                connection.commit()

                if cursor.rowcount == 1:
                    print("Scholarship in Row commited Successfully")
            
    except Error as e:
        print(e)

    return render_template('home.html')
    

@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    first = request.form.get('fName')
    last = request.form.get('lName')
    grade = request.form.get('classification')
    rand = random.randint(10000000, 99999999)
    dob = request.form.get('birthDay')

    # Convert MM/DD/YYYY to YYYY-MM-DD
    formatted_dob = datetime.strptime(dob, '%m-%d-%Y').strftime('%Y-%m-%d')
    print(formatted_dob)
    print(rand)

    uName = (first[:3]+last[0]).lower()+formatted_dob[-2:]
    print(uName)

    #database connectivity
    try:
        with connect(
 host = "",
user = "",
password = "",
database = ""

        ) as connection:
            insert_query1 = """
                            INSERT INTO Student (student_id, first_name, last_name, classification, date_of_bith, created_at) 
                            VALUES (%s, %s, %s, %s, %s, NOW());
                           """
            insert_query2 = '''
                            INSERT INTO billing (student_id, username, totalAmount, amountPaid, billRem, fyear) 
                            VALUES (%s, %s, %s, %s, %s,%s);
                            '''
            insert_query3 = """
                               INSERT INTO scholarship (student_id, username, amount, fyear) 
                                VALUES (%s, %s, %s, %s); 

                                """
            
            with connection.cursor() as cursor:
                cursor.execute(insert_query1, (rand, first, last, grade, formatted_dob))
                cursor.execute(insert_query2, (rand, uName, 11000, 0, 11000, 2025))
                cursor.execute(insert_query3, (rand,uName, 0, 2025 ) )
                #cursor.execute()
                connection.commit()
                print(f"Row inserted successfully.")

    except Error as e:
        print(e)

    return render_template('result.html', fName = first, lName = last, studentID =rand, userName= uName)


print(__name__)
if __name__ == "__main__":
    
    app.run(host="0.0.0.0",port=5555, debug=True)



