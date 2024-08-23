from io import BytesIO
from flask import Flask, request, jsonify, send_file
from flask_mysqldb import MySQL
# import awsgi


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'usermanagement'
mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def register():
  try:
        required_fields = ['Employee_ID', 'Username', 'Password']
        for field in required_fields:
            if field not in request.form:
                return jsonify({'error': f'Missing required form field: {field}'}), 400
        Employee_ID = request.form['Employee_ID']
        Full_Name = request.form.get('Full_Name', '')
        Email_Address = request.form.get('Email_Address', '')
        Username = request.form['Username']
        Password = request.form['Password']
        Gender = request.form.get('Gender', '')
        Manager = request.form.get('Manager', '')
        Mobile_No = request.form.get('Mobile_No', '')
        Role = request.form.get('Role', '')
        if 'image' not in request.files or not request.files['image'].filename:
            return jsonify({'error': 'No image file uploaded or image field is missing'}), 400
        image = request.files['image']
        image_data = image.read()
        cur = mysql.connection.cursor()
        cur.execute ("INSERT INTO user (Employee_ID, Full_Name, Email_Address, Username, Password, Gender, Manager, Mobile_No, Role, image)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (Employee_ID, Full_Name, Email_Address, Username, Password, Gender, Manager, Mobile_No, Role, image_data))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'User registered successfully'}), 200
  except Exception as e:
        print("Exception:", str(e))  
        return jsonify({'error': 'Internal server error: ' + str(e)}), 500




# @app.route('/register', methods=['POST'])
# def register():
#     try:
#         if 'id' not in request.form or 'name' not in request.form or 'mobile_no' not in request.form:
#             return jsonify({'error': 'Missing required form fields'}), 400

#         id = request.form['id']
#         name = request.form['name']
#         mobile_no = request.form['mobile_no']

#         if 'image' not in request.files or request.files['image'].filename == '':
#             return jsonify({'error': 'No image file uploaded'}), 400

#         image = request.files['image']
#         image_data = image.read()

#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO user (id, name, mobile_no, image) VALUES (%s, %s, %s, %s)",
#                      (id, name, mobile_no, image_data))
#         mysql.connection.commit()
#         cur.close()

#         return jsonify({'message': 'User registered successfully'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @app.route('/register/<int:id>', methods=['GET'])
# def get_user_by_register(id):
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT id, name, mobile_no, image FROM user WHERE id = %s", (id,))
#         user = cur.fetchone()
#         cur.close()

#         if user:
#             user_dict = {
#                 'id': user[0],
#                 'name': user[1],
#                 'mobile_no': user[2],
#                 'image_url': f'/image/{id}'  # URL to fetch the image
#             }
#             return jsonify({'user': user_dict})
#         else:
#             return jsonify({'message': f'User with id {id} not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/image/<int:id>', methods=['GET'])
# def get_image(id):
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT image FROM user WHERE id = %s", (id,))
#         result = cur.fetchone()
#         cur.close()
#         if result and result[0]:
#             image_data = result[0]
#             return send_file(
#                 BytesIO(image_data),
#                 mimetype='image/jpeg',  # Adjust this based on your image type (e.g., 'image/png')
#                 as_attachment=False,
#                 download_name='image.jpg'  # Updated argument for file name
#             )
#         else:
#             return jsonify({'message': 'Image not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500



@app.route('/register/<int:Employee_ID>', methods=['GET'])
def get_user_by_register(Employee_ID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT Employee_ID, Full_Name, Email_Address, Username, Password, Gender, Manager, Mobile_No, Role, image FROM USER WHERE Employee_ID = %s",(Employee_ID,))
        user = cur.fetchone()
        cur.close()

        if user:
            user_dict = {
                'Employee_ID': user[0],
                'Full_Name': user[1],
                'Username': user[2],
                'Password':user[3],
                'Gender':user[4],
                'Manager':user[5],
                'Mobile_No':user[6],
                'Role':user[7],
                'image_url': f'/image/{Employee_ID}'  # URL to fetch the image
            }
            return jsonify({'user': user_dict})
        else:
            return jsonify({'message': f'User with id {id} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/image/<int:Employee_ID>', methods=['GET'])
def get_image(Employee_ID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT image FROM user WHERE Employee_ID = %s", (Employee_ID,))
        result = cur.fetchone()
        cur.close()
        if result and result[0]:
            image_data = result[0]
            return send_file(
                BytesIO(image_data),
                mimetype='image/jpeg',  # Adjust this based on your image type (e.g., 'image/png')
                as_attachment=False,
                download_name='image.jpg'  # Updated argument for file name
            )
        else:
            return jsonify({'message': 'Image not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/register/<int:Employee_ID>', methods=['PUT'])
# def update_user_by_register(Employee_ID):
#     try:
#         if 'image' in request.files:
#             image = request.files['image']
#             image_data = image.read()
#         else:
#             image_data = None
#         Employee_ID=request.form.get('Employee_ID')
#         Full_Name = request.form.get('Full_Name')
#         Username = request.form.get('Username')
#         Password = request.form.get('Password')
#         Gender = request.form.get('Gender')
#         Manager = request.form.get('Manager')
#         Mobile_No = request.form.get('Mobile_No')
#         Role = request.form.get('Role')
#         cur = mysql.connection.cursor()
#         if image_data:
#             cur.execute("UPDATE user SET Employee_ID = %s, Full_Name = %s, Username = %s, Password = %s Gender = %s Manager = %s Mobile_No = %s Role= %s WHERE id = %s",
#                         (Employee_ID, Full_Name, Username, Password,Gender,Manager,Mobile_No, Role ,image_data, id))
#         else:
#             cur.execute("UPDATE user SET Employee_ID = %s, Full_Name = %s, Username = %s, Password = %s Gender = %s Manager = %s Mobile_No = %s Role= %s WHERE id = %s",
#                         (Employee_ID, Full_Name, Username, Password,Gender,Manager,Mobile_No, Role ,image_data, id))
#         mysql.connection.commit()
#         cur.close()
#         return jsonify({'message': 'User updated successfully'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500



# @app.route('/register/<int:id>', methods=['PUT'])
# def update_register(id):
#     try:
#         if 'image' in request.files:
#             image = request.files['image']
#             image_data = image.read()
#         else:
#             image_data = None
#         new_id=request.form.get('id')
#         name = request.form.get('name')
#         mobile_no = request.form.get('mobile_no')
#         cur = mysql.connection.cursor()
#         if image_data:
#             cur.execute("UPDATE user SET id = %s, name = %s, mobile_no = %s, image = %s WHERE id = %s",
#                         (new_id, name, mobile_no, image_data, id))
#         else:
#             cur.execute("UPDATE user SET name = %s, mobile_no = %s WHERE id = %s",
#                         (new_id, name, mobile_no, id))
#         mysql.connection.commit()
#         cur.close()
#         return jsonify({'message': 'User updated successfully'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/register/<int:id>', methods=['DELETE'])
# def delete_register(id):
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute("DELETE FROM user WHERE id = %s", (id,))
#         mysql.connection.commit()
#         cur.close()
#         return jsonify({'message': 'User deleted successfully'})
#     except Exception as e:
#         return jsonify({'error': str(e)})

# def lambda_handelr(event, context):
#     return awsgi.response(app, event, context, base64_content_types={"image/png"})


if __name__ == '__main__':
    app.run(debug=True)