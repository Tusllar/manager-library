
from flask import Blueprint, render_template, request, flash, session
from flask_login import login_required, current_user
from .models import User_infor,File,Server,User,Class,UserClass
from flask import Blueprint, render_template, flash, request, jsonify,redirect,url_for,session
from . import db
from datetime import datetime

lecturers = Blueprint("lecturers", __name__)  


@lecturers.route("/lecturer",methods=["GET","POST"])
def lecturer():
      user_files = File.query.filter_by(user_id=current_user.id).all()    
      user_info = User_infor.query.filter_by(user_id=current_user.id).first()
      classes = Class.query.all()
      print(current_user.role)
    #   files = File.query.filter_by(status='pending').all() 
      return render_template("lecturer.html", user=current_user,user_info=user_info,user_files=user_files,classes=classes)
@lecturers.route('/create_class', methods=['POST'])
def create_class():
    # Lấy dữ liệu từ biểu mẫu
    class_name = request.form['class_name']
    description = request.form['description']
    print(class_name,description)
    # Kiểm tra tên lớp có tồn tại chưa
    existing_class = Class.query.filter_by(name=class_name).first()
    if existing_class:
        flash('Tên lớp đã tồn tại!', category='error')
        return redirect(url_for('lecturers.lecturer'))
    
    # Tạo lớp học mới
    new_class = Class(name=class_name, description=description)
    db.session.add(new_class)
    db.session.commit()

    user = current_user  # Giả sử bạn dùng Flask-Login để quản lý phiên đăng nhập
    user.classes.append(new_class)  # Thêm lớp vào danh sách lớp của user
    db.session.commit()

    flash('Lớp học được tạo thành công!', category='success')
    return redirect(url_for('lecturers.lecturer'))
@lecturers.route('/delete_class/<int:class_id>', methods=['POST'])
def delete_class(class_id):
    cls = Class.query.get(class_id)
    if not cls:
        flash('Lớp học không tồn tại!', category='error')
        return redirect(url_for('lecturers.lecturer'))
    # Xóa lớp học
    db.session.delete(cls)
    db.session.commit()
    flash('Lớp học đã được xóa!', category='success')
    return redirect(url_for('lecturers.lecturer'))

@lecturers.route('/class_details/<int:class_id>', methods=['GET'])
def class_details(class_id):
    user_files = File.query.filter_by(user_id=current_user.id).all()    
    user_info = User_infor.query.filter_by(user_id=current_user.id).first()
    class_details = Class.query.get(class_id)  # Lấy lớp học theo class_id
    if class_details:
        students = [user for user in class_details.users if user.id != current_user.id]
        # students = class_details.users  # Lấy danh sách sinh viên tham gia lớp (từ bảng users)
        return render_template('list_student_class.html',user=current_user,user_info=user_info,user_files=user_files,class_details=class_details, students=students)
    else:
        flash("Class not found.")
        return redirect('/lecturer')  

@lecturers.route('/view_file_student/<int:id>',methods = ['GET'])
def view_file_student(id):
    # user_id = request.form['user_id']
    # user_id = request.args.get('user_id')
    # print(user_id)
    print(id) 
    user_info = User_infor.query.filter_by(user_id=current_user.id).first()
    # = User.query.filter_by(user_id=user_id).first()
    student =User_infor.query.filter_by(user_id=id).first()
    print('k có à')
    print(id)
    print(student)
    user_files = File.query.filter_by(user_id=id,status = 'approved').all()
    print(user_files)
    return render_template('lecturer_view_file_student.html',user=current_user,user_files=user_files,user_info=user_info,student=student)