import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime, date


app = Flask(__name__)
CORS(app)


# Post Data
@app.route('/post', methods=['POST'])
def post_data():
    data = request.json
    conn = psycopg2.connect(
        host='localhost',
        database='pharmacyDb',
        user='postgres',
        password='password',
        port=5432
    )
    cur = conn.cursor()

    # data_json = json.dumps(data)
    sql = "INSERT INTO users (user_code, fullname, email, password, is_active, num_permission, created_on, last_login) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql, (data['user_code'], data['fullname'], data['email'], data['password'],
                data['is_active'], data['num_permission'], data['created_on'], data['last_login']))
    conn.commit()

    cur.close()
    conn.close()
    response = jsonify({'status': 'success'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    # return {'message': 'Data posted successfully'}

# Get ALL


@app.route('/api', methods=['GET'])
def get_data():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='pharmacyDb',
            user='postgres',
            password='password',
            port=5432
        )
        cur = conn.cursor()
        query = '''SELECT * FROM users'''
        data = []

        cur.execute(query)
        results = cur.fetchall()
        for row in results:
            data.append(
                {
                    'user_Code': row[0],
                    'name': row[1],
                    'email': row[2],
                    'is_active': row[4],
                    'num_permission':row[5],
                    'created_on':row[6],
                    'last_login':row[7]
                })
        cur.close()
        conn.close()
        return data
    except (Exception, psycopg2.Error) as error:
        print(error)
        return jsonify({'error': 'Failed to fetch data from database'}), 500
    

 
#Fetch by date
@app.route('/getbydate', methods=['GET'])
def get_result():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='pharmacyDb',
            user='postgres',
            password='password',
            port=5432
        )
        cur = conn.cursor()
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        cur.execute("SELECT * FROM users WHERE created_on BETWEEN %s AND %s", (start_date, end_date))
        data_by_date = []
        res = cur.fetchall()
        for row in res:
            data_by_date.append(
                {
                    'user_Code': row[0],
                    'name': row[1],
                    'email': row[2],
                    'is_active': row[4],
                    'num_permission':row[5],
                    'created_on':row[6],
                    'last_login':row[7]
                })
        cur.close()
        return jsonify(data_by_date)
    
    except (Exception, psycopg2.Error) as error:
        print(error)
        return jsonify({'error': 'Failed to fetch data from database'}), 500



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
