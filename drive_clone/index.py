import os
from datetime import date
import stripe
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, redirect, request, jsonify, send_file
from drive_clone import app, dao, login_manager


### Get total storage --------------------------------------------------------------------------
def get_total_storage():
    total_storage_used = dao.get_total_storage_used(user_id=current_user.id) or 0
    total_storage = dao.get_total_storage(user_id=current_user.id) or 0
    return float(total_storage_used), float(total_storage)


### Landing page-------------------------------------------------------------------------------------
@app.route("/")
def landing():
    return render_template("landing.html")


### Login-------------------------------------------------------------------------------------
@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect("/main")
    return render_template("login/login.html")


@app.route("/api/login", methods=['POST'])
def login_process():
    email = request.json.get('email')
    password = request.json.get('password')

    user = dao.user_auth(email, password)

    if user:
        login_user(user=user)
        return jsonify({"message": "Đăng nhập thành công", "status": 200, 'redirect': '/main'})
    else:
        return jsonify({"message": "Email hoặc mật khẩu không đúng", "status": 401})


@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


### Logout-------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


### Register-------------------------------------------------------------------------------------
@app.route("/register")
def register():
    return render_template('register/register.html')


@app.route("/api/register", methods=["POST"])
def register_process():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    if dao.is_email_exist(email=email):
        return jsonify({'message': 'Email đã được đăng ký', 'status': 400})

    if dao.add_user(name=name, email=email, password=password):
        return jsonify({
            'message': 'Đăng ký thành công',
            'status': 200,
            'redirect': '/login'
        })
    else:
        return jsonify({
            'message': "Đăng ký không thành công! Vui lòng kiểm tra lại thông tin!",
            'status': 400
        })


### Main-------------------------------------------------------------------------------------
@app.route("/main")
@login_required
def main():
    name = request.args.get('name')
    type = request.args.get('file_type')
    files = dao.load_user_files(user_id=current_user.id, name=name,file_type=type) or []
    file_type = dao.get_all_file_type() or []

    total_storage_used, total_storage = get_total_storage()
    return render_template("main/main.html", files=files, total_storage_used=total_storage_used,
                           total_storage=total_storage, file_type=file_type)


### Upload file-------------------------------------------------------------------------------------
@app.route("/api/upload", methods=['POST'])
@login_required
def upload():
    file = request.files['file']
    upload_folder = app.config['UPLOAD_FOLDER']
    total_storage_used, total_storage = get_total_storage()

    remaining_storage = total_storage - total_storage_used
    file_size = len(file.read()) / (1024 * 1024)
    file.seek(0)

    if file_size > remaining_storage:
        return {"success": False, "message": "Dung lượng còn lại không đủ để tải file này", "status": 400}

    user_folder = os.path.join(upload_folder, str(current_user.id))
    os.makedirs(user_folder, exist_ok=True)

    filename, file_extension = os.path.splitext(file.filename)
    file_path = os.path.abspath(os.path.join(user_folder, filename + file_extension))

    if dao.is_file_exist(file_name=filename, user_id=current_user.id):
        return {"success": False, "message": "File " + file.filename + " đã tồn tại trong hệ thống", "status": 409}

    file.save(file_path)

    file_type = file_extension.lstrip('.')
    result = dao.add_file(file_name=filename, file_path=file_path, file_size=file_size, file_type=file_type,
                          user_id=current_user.id)

    if result:
        return {"success": True, "message": "Tải file " + file.filename + " lên hệ thống thành công"}
    else:
        return {"success": False, "message": "Tải file thất bại"}


### Delete file-------------------------------------------------------------------------------------
@app.route("/api/delete_file/<int:file_id>", methods=["DELETE"])
@login_required
def delete_file_process(file_id):
    file = dao.get_file_by_id(file_id=file_id)

    if not file:
        return {"success": False, "message": "Không tìm thấy file trên hệ thống"}

    if os.path.exists(file.file_path):
        os.remove(file.file_path)

    if dao.delete_file(file_id=file_id):
        return {"success": True, "message": "Xoá file thành công"}
    else:
        return {"success": False, "message": "Gặp lỗi! Vui lòng thử lại"}


### Download file-------------------------------------------------------------------------------------
@app.route("/api/download_file/<int:file_id>", methods=['GET'])
@login_required
def download_file_process(file_id):
    file = dao.get_file_by_id(file_id=file_id)

    return send_file(file.file_path, as_attachment=True)


### Rename file-------------------------------------------------------------------------------------
@app.route('/api/rename_file/<int:file_id>', methods=['POST'])
@login_required
def rename_file(file_id):
    new_name = request.json.get('new_name')
    file = dao.get_file_by_id(file_id=file_id)

    if not file:
        return jsonify({"success": False, "message": "Không tìm thấy file"})

    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id))
    file_type = file.file_type
    old_file_path = file.file_path
    new_file_path = os.path.join(user_folder, new_name + "." + file_type)

    if not os.path.exists(old_file_path):
        return jsonify({"success": False, "message": "File gốc không tồn tại"})

    os.rename(old_file_path, new_file_path)
    result = dao.rename_file(file_id=file_id, new_file_name=new_name, new_file_path=new_file_path)
    if result:
        return jsonify({"success": True, "message": "Đổi tên file thành công"})
    else:
        return jsonify({"success": False, "message": "Gặp lỗi! Vui lòng thực hiện lại"})


### Upgrade storage-------------------------------------------------------------------------------------
@app.route("/upgrade")
def upgrade():
    return render_template("payment/upgrade.html")


### Payment---------------------------------------------------------------------------------------------
@app.route('/create_checkout_session', methods=['POST'])
def create_checkout_session():
    stripe.api_key = app.config['STRIPE_API_KEY_PRIVATE']
    size = request.json.get('size')
    price = request.json.get('price')

    domain = app.config["DOMAIN"]

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'{size} GB Storage Upgrade',
                    },
                    'unit_amount': int(int(price) * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            metadata={
                'size': str(size),
                'price': str(price)
            },
            success_url= f'http://{domain}/payment_success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url= f'http://{domain}/payment_cancel',
        )

        return jsonify({"success": True, 'checkout_url': session.url})

    except Exception as e:
        return jsonify({"success": False, 'error': f"Lỗi khi tạo phiên thanh toán: {str(e)}"})


@app.route('/payment_success')
def payment_success():
    stripe.api_key = app.config['STRIPE_API_KEY_PRIVATE']
    session_id = request.args.get('session_id')

    if not session_id:
        return "Thiếu session ID", 400

    try:
        session = stripe.checkout.Session.retrieve(
            session_id,
            expand=['line_items', 'payment_intent']
        )

        size = session['metadata'].get('size')
        price = session['metadata'].get('price')
        payment_intent = session.get('payment_intent')
        transaction_id = payment_intent['id'] if payment_intent else 'N/A'

        result = dao.add_storage_purchase(user_id=current_user.id, size=size, price=price)
        today = date.today()

        if result:
            return render_template("payment/success.html", price=price, size=size, date=today, id=transaction_id)
        else:
            return "Thanh toán thành công nhưng có lỗi khi lưu dữ liệu vào hệ thống.", 500

    except Exception as e:
        return f"Lỗi khi xác minh phiên thanh toán: {str(e)}", 500


@app.route('/payment_cancel')
def payment_cancel():
    today = date.today()
    return render_template("payment/cancel.html", date=today)


@app.route('/history_payment')
def history_payment():
    history_pay = dao.get_history_payment(current_user.id) or []
    return render_template("payment/history.html", history_pay=history_pay)


if __name__ == '__main__':
    app.run(debug=True)
