
from flask import Blueprint, render_template, request, flash, session
from flask_login import login_required, current_user
from .models import User_infor,File,Server,User,Class,UserClass
from flask import Blueprint, render_template, flash, request, jsonify,redirect,url_for,session
from . import db
from datetime import datetime
admins = Blueprint("admins", __name__)  

@admins.route("/admin",methods=["GET","POST"])
@login_required
def admin():
      user_files = File.query.filter_by(user_id=current_user.id).all()    
      user_info = User_infor.query.filter_by(user_id=current_user.id).first()
      print(current_user.role)
      files = File.query.filter_by(status='pending').all() 
      return render_template("admin.html", user=current_user,user_info=user_info,user_files=user_files,files=files)

@admins.route("/admin_manager",methods=["GET","POST"])
@login_required
def admin_manager():
      user_files = File.query.filter_by(user_id=current_user.id).all()    
      user_info = User_infor.query.filter_by(user_id=current_user.id).first()
      users = User.query.filter(User.id != current_user.id).all()
      print(users)
      for i in users:
          print(i.id,i.user_name,i.email,i.role)
       
      print(current_user.role)
      files = File.query.filter_by(status='pending').all() 
      return render_template("user_management.html", user=current_user,user_info=user_info,user_files=user_files,files=files,users=users)

@admins.route('/approve_file/<int:file_id>', methods=['POST'])
@login_required
def approve_file(file_id):
 
    file = File.query.get_or_404(file_id)
   
    print(file_id)
    file.status = 'approved'  # Duyệt file
    
    file.approval_time = datetime.utcnow()
    db.session.commit()
    flash('File approved successfully!', category='success')
    return redirect(url_for('admins.admin'))

@admins.route('/reject_file/<int:file_id>', methods=['POST'])
@login_required
def reject_file(file_id):
    print(file_id)
    file = File.query.get_or_404(file_id)
  
    file.status = 'rejected'  # Từ chối file
    
    file.approval_time = None

    db.session.commit()
    flash('File rejected.', category='error')
    return redirect(url_for('admins.admin'))


@admins.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    print(user_id)
    # Tìm user theo ID
    user = User.query.get(user_id)
    if not user:
        flash("Không tìm thấy người dùng.", "warning")
        return redirect(url_for('admins.admin_manager'))  # Trả về danh sách user hoặc trang chính

    try:
        # Xóa user
        db.session.delete(user)
        db.session.commit()
        flash("Người dùng đã được xóa thành công.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Đã xảy ra lỗi: {str(e)}", "danger")

    return redirect(url_for('admins.admin_manager'))
