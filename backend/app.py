from flask import Flask, request, jsonify
from models import db, init_db, Operation
from auth import auth_required
from utils import get_current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/start', methods=['POST'])
@auth_required
def start_operation():
    data = request.json
    op = Operation(
        worker_id=data['worker_id'],
        order_number=data['order_number'],
        start_time=db.func.current_timestamp()
    )
    db.session.add(op)
    db.session.commit()
    return jsonify({"status": "started", "id": op.id})

@app.route('/stop/<int:op_id>', methods=['POST'])
@auth_required
def stop_operation(op_id):
    op = Operation.query.get(op_id)
    if op and not op.end_time:
        op.end_time = db.func.current_timestamp()
        db.session.commit()
        return jsonify({"status": "stopped", "id": op.id})
    return jsonify({"error": "Invalid operation ID or already stopped"}), 400

@app.route('/operations', methods=['GET'])
@auth_required
def list_operations():
    user = get_current_user()
    ops = Operation.query

    if not user['is_admin']:
        ops = ops.filter_by(worker_id=user['username'])

    # Filter podľa dátumu
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    if date_from:
        from_dt = datetime.strptime(date_from, "%Y-%m-%d")
        ops = ops.filter(Operation.start_time >= from_dt)
    if date_to:
        to_dt = datetime.strptime(date_to, "%Y-%m-%d")
        ops = ops.filter(Operation.start_time <= to_dt)

    return jsonify([op.to_dict() for op in ops.all()])


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)

import csv
from io import StringIO
from flask import Response
from datetime import datetime


@app.route('/export', methods=['GET'])
@auth_required
def export_operations():
    user = get_current_user()
    ops = Operation.query

    if not user['is_admin']:
        ops = ops.filter_by(worker_id=user['username'])

    # Filtrovanie podľa dátumu
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    if date_from:
        from_dt = datetime.strptime(date_from, "%Y-%m-%d")
        ops = ops.filter(Operation.start_time >= from_dt)
    if date_to:
        to_dt = datetime.strptime(date_to, "%Y-%m-%d")
        ops = ops.filter(Operation.start_time <= to_dt)

    # Vytvorenie CSV
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(["ID", "Worker ID", "Order Number", "Start Time", "End Time"])
    for op in ops.all():
        cw.writerow([
            op.id,
            op.worker_id,
            op.order_number,
            op.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            op.end_time.strftime("%Y-%m-%d %H:%M:%S") if op.end_time else ""
        ])

    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=operacie.csv"}
    )

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    from models import User
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "User already exists"}), 400
    new_user = User(username=data['username'], is_admin=data.get('is_admin', False))
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "user created"})
