import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)
#Post Data

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
        query = '''SELECT * FROM users 
                   WHERE is_active = true'''
        data = []

        cur.execute(query)
        results = cur.fetchall()
        for row in results:
            data.append(
                {
                    'user_Code': row[0],
                    'name': row[1],
                    'email': row[2]
                })
        cur.close()
        conn.close()
        return data
    except (Exception, psycopg2.Error) as error:
        print(error)
        return jsonify({'error': 'Failed to fetch data from database'}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
