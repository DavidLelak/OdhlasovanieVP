from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
from io import StringIO
from models import db, Operation, User
from auth import auth_required
from utils import get_current_user
from fastapi.responses import FileResponse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/operations/start', methods=['POST'])
@auth_required
def start_operation():
    data = request.json
    op = Operation(
        worker_id=data['worker_id'],
        order_number=data['order_number'],
        start_time=datetime.now()
    )
    db.session.add(op)
    db.session.commit()
    return jsonify(op.to_dict()), 201

@app.route('/operations/stop/<int:op_id>', methods=['POST'])
@auth_required
def stop_operation(op_id):
    op = Operation.query.get_or_404(op_id)
    op.end_time = datetime.now()
    db.session.commit()
    return jsonify(op.to_dict())

@app.route('/operations', methods=['GET'])
@auth_required
def list_operations():
    user = get_current_user()
    ops = Operation.query
    if not user['is_admin']:
        ops = ops.filter_by(worker_id=user['username'])
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    if date_from:
        from_dt = datetime.strptime(date_from, "%Y-%m-%d")
        ops = ops.filter(Operation.start_time >= from_dt)
    if date_to:
        to_dt = datetime.strptime(date_to, "%Y-%m-%d")
        ops = ops.filter(Operation.start_time <= to_dt)
    return jsonify([op.to_dict() for op in ops.all()])

@app.route('/export', methods=['GET'])
@auth_required
def export_operations():
    user = get_current_user()
    ops = Operation.query
    if not user['is_admin']:
        ops = ops.filter_by(worker_id=user['username'])
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    if date_from:
        from_dt = datetime.strptime(date_from, "%Y-%m-%d")
        ops = ops.filter(Operation.start_time >= from_dt)
    if date_to:
        to_dt = datetime.strptime(date_to, "%Y-%m-%d")
        ops = ops.filter(Operation.start_time <= to_dt)
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
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "User already exists"}), 400
    new_user = User(username=data['username'], is_admin=data.get('is_admin', False))
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "user created"})

if __name__ == '__main__':
    app.run(debug=True)

# pridanie cesty pre favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")