from math import e
from flask import jsonify
from re import template
from flask import Blueprint, render_template, request, flash, session
from flask.helpers import url_for
from sqlalchemy.sql.expression import false
from werkzeug.utils import redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from todolist import views
from .models import User,User_infor,File
user = Blueprint("user", __name__)
from . import db
import mysql.connector
from mysql.connector import Error
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',  
        user='root',      
        password='xxxxx',  
        database='xxxxx'
    )
    return conn

@user.route('/check',methods=['POST','GET'])
def check_file():
    que = request.args.get('query', '').lower()
    print(que)
    conn = get_db_connection()
    cur = conn.cursor()
    # query = "SELECT *FROM Server"
    query = "SELECT *FROM file"
    cur.execute(query)
    data = cur.fetchall()
    data_list = [list(row) for row in data]
    # In kết quả
    for item in data_list:
        print(item)
    if que:
 
       filtered_data = [
                            row for row in data_list
                            if (que in str(row[2]).lower() or que in str(row[3]).lower() or que in str(row[4]).lower()) and row[16] == 'approved' and row[9] == '.pdf'
                       ]

    else:
        filtered_data = data
    print('done')    
    print(filtered_data)
    # Trả về dữ liệu dưới dạng JSON
    return jsonify(filtered_data)

@user.route('/information', methods=["GET", "POST"])
@login_required
def information():
    if request.method == "POST":
        # Lấy dữ liệu từ form
        full_name = request.form.get("full_name")
        user_class = request.form.get("class")
        age = request.form.get("age")
        phone = request.form.get("phone")
        address = request.form.get("address")
        gender = request.form.get("gender")

        # Kiểm tra xem người dùng đã có thông tin chưa
        user_info = User_infor.query.filter_by(user_id=current_user.id).first()
        
        if user_info:
            # Cập nhật thông tin người dùng nếu đã có thông tin
            user_info.full_name = full_name
            user_info.c_class = user_class
            user_info.age = age
            user_info.phone = phone
            user_info.address = address
            user_info.gender = gender
            db.session.commit()
            flash("Information updated successfully!", category="success")
        else:
            # Nếu chưa có thông tin, tạo mới thông tin người dùng
            new_info = User_infor(
                full_name=full_name, 
                email=current_user.email, 
                age=age,
                c_class=user_class, 
                phone=phone,
                address=address, 
                gender=gender, 
                user_id=current_user.id
            )
            db.session.add(new_info)
            db.session.commit()
            flash("Information added successfully!", category="success")

        # Sau khi xử lý xong, quay lại trang thông tin người dùng
        return redirect(url_for("user.information"))
    
    # Hiển thị form nhập thông tin, lấy thông tin người dùng nếu đã có
    user_info = User_infor.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', user_info=user_info,user=current_user)

@user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(email,password)
        user = User.query.filter_by(email=email).first()
        if user:
        
            if check_password_hash(user.password, password):
                print("hoo")
                session.permanent = True
                login_user(user, remember=True)
                flash("Logged in success!", category="success")
                if user.role =='student':
                   return redirect(url_for("views.homedash"))
                elif user.role == 'lecturer':
                    return redirect(url_for("lecturers.lecturer"))
                elif user.role == 'admin':
                    return redirect(url_for("admins.admin"))
            else:
                print("SAI À")
                flash("Wrong password, please check again!", category="error")
        else:
            flash("User doesn't exist!", category="error")
    return render_template("login.html", user=current_user)

@user.route("/forgot",methods = ['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')

        user = User.query.filter_by(email = email).first()
        if user:
            session['email'] = email
            flash("Password reset link sent to your email!", category="success")
            return redirect(url_for('user.register_password'))
        else:
            flash("User doesn't exist!", category="error")
            return render_template('forgot.html')
        
    return render_template('forgot.html')


@user.route("/register_pass",methods = ['GET','POST'])
def register_password():
    email = session.get('email') 
    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        print(new_password,confirm_password)
        user = User.query.filter_by(email=email).first()
        if new_password == confirm_password:
            print(new_password)
            user.password = generate_password_hash(new_password,method="pbkdf2:sha256")
            # user.password = new_password
            db.session.commit()
            flash("Password changed successfully!", category="success")
            return redirect(url_for('user.login'))
        else:
            flash("Passwords don't match!", category="error")
            print('loi à')
            return render_template('register.html')
       
    return render_template('register.html')
@user.route("/change_pass",methods = ['GET','POST'])
def change_password():
    user_files = File.query.filter_by(user_id=current_user.id).all()    
    user_info = User_infor.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        print(old_password,new_password,confirm_password)
       
        if check_password_hash(current_user.password, old_password):
            if new_password == confirm_password:
                current_user.password = generate_password_hash(new_password,method="pbkdf2:sha256")
                db.session.commit()
                flash("Password changed successfully!", category="success")
                return redirect(url_for('views.homedash'))
            else:
                flash("Passwords don't match!", category="error")
                return render_template('changepass.html',user=current_user,user_info=user_info,user_files=user_files)
        else:
            flash("Old password is incorrect!", category="error")
            return render_template('changepass.html',user=current_user,user_info=user_info,user_files=user_files)
        
    return render_template('changepass.html',user=current_user,user_info=user_info,user_files=user_files)

@user.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form['role']
        print(role)
        print(email,password)
        user = User.query.filter_by(email=email).first()
        # validate user
        if user:
            flash("User existed!", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(password) < 7:
            flash("Email must be greater than 7 characters.", category="error")
        elif password != confirm_password:
            flash("Password doesn not match!", category="error")
        else:
            password = generate_password_hash(password, method="pbkdf2:sha256")
            new_user = User(email, password, user_name, role)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("User created!", category="success")
                login_user(new_user, remember=True)  # Chắc chắn sử dụng new_user, không phải user
                return redirect(url_for("views.homedash"))
            except Exception as e:
                flash("Error when creating user!", category="error")
                print(f"Error: {e}")
                return render_template("login.html", user=current_user)

    return render_template("login.html", user=current_user)

@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))


    
    