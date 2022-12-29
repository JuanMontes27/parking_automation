from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from parking_payment.db import get_db
from datetime import datetime

bp = Blueprint('vehicles', __name__)

@bp.route('/')
def index():
    db = get_db()
    vehicles = db.execute(
        'SELECT * FROM vehicles '
        'INNER JOIN vehicle_types '
        'ON vehicles.vehicle_type_id = vehicle_types.id'
    ).fetchall()
    return render_template('vehicles/index.html', vehicles=vehicles)

@bp.route('/create-type', methods=('GET', 'POST'))
def create_type():
    if request.method == 'POST':
        vehicle_type = request.form['new-type']
        payment = request.form['payment']
        error = None
        db = get_db()

        if not vehicle_type:
            error = 'Favor de ingresar el nuevo tipo de vehiculo'
        elif not payment:
            error = 'Favor de ingresar el cobro por minuto'
        
        if error is None:
            try:
                db.execute(
                    'INSERT INTO vehicle_types (vehicle_type, payment)'
                    ' VALUES (?, ?)',
                    (vehicle_type, float(payment))
                )
                db.commit()
            except db.IntegrityError:
                error = f'El tipo de placas: {vehicle_type} ya ha sido registrada'
            else:
                return redirect(url_for('vehicles.index'))
        flash(error)
    return render_template('vehicles/create-type.html')

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        plate_number = request.form['plate']
        vehicle_type = request.form['type']
        error = None

        if not plate_number:
            error = 'Favor de ingresar el numero de placas'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO vehicles (vehicle_type_id, plate_number, date_start)'
                ' VALUES (?, ?, ?)',
                (vehicle_type, plate_number, str(datetime.today()))
            )
            db.commit()
            return redirect(url_for('vehicles.index'))
    db = get_db()
    payments = db.execute(
        'SELECT * FROM vehicle_types'
    ).fetchall()
    return render_template('vehicles/create.html', payments=payments)

@bp.route('/<int:id>/collect', methods=('GET', 'POST'))
def collect(id):
    db = get_db()
    vehicle = db.execute(
        'SELECT * FROM vehicles '
        'INNER JOIN vehicle_types '
        'ON vehicles.vehicle_type_id = vehicle_types.id '
        'WHERE vehicles.id=?',
        (id, )
    ).fetchone()

    date_format_str = '%Y-%m-%d %H:%M:%S.%f'
    date_start = datetime.strptime(vehicle['date_start'], date_format_str)
    date_end = datetime.today()
    difference_min = round((date_end - date_start).total_seconds() / 60)
    payment_parking = difference_min * vehicle['payment']
    info_vehicle = {
        'plate_number': vehicle['plate_number'],
        'date_start': vehicle['date_start'],
        'date_end': str(date_end),
        'parked_time': str(difference_min),
        'vehicle_type': vehicle['vehicle_type'],
        'payment_type': vehicle['payment'],
        'payment_parking': payment_parking,
    }

    if request.method == 'POST':
        db.execute(
            'UPDATE vehicles SET date_end=?, parked_time=?, payment_parking=? '
            'WHERE id=?',
            (info_vehicle['date_end'], info_vehicle['parked_time'], info_vehicle['payment_parking'], id)
        )
        db.commit()
        return redirect(url_for('vehicles.index'))
    return render_template('vehicles/collect.html', info_vehicle=info_vehicle)

@bp.route('/vehicles-registration', methods=('GET', 'POST'))
def vehicles_registration():
    db = get_db()
    records = db.execute(
        'SELECT plate_number, payment_parking, vehicle_type, payment_parking FROM vehicles '
        'INNER JOIN vehicle_types '
        'ON vehicles.vehicle_type_id = vehicle_types.id '
        'WHERE payment_parking IS NOT NULL'
    ).fetchall()
    return render_template('vehicles/registration.html', records=records)
