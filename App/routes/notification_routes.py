from . import main
from flask import request, jsonify
from flask_login import login_required, current_user
from ..decorators import email_verified_required
from .. import db
from sqlalchemy.orm.attributes import flag_modified

@main.route('/delete_notification', methods=['POST'])
@login_required
@email_verified_required
def delete_notification():
    data = request.get_json()
    notification = data.get('notif')
    if notification in current_user.notifaction_data['deleted']:
        current_user.notifaction_data['deleted'].remove(notification)
        flag_modified(current_user, "notifaction_data")
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})

@main.route('/get_notifications', methods=['GET'])
@login_required
@email_verified_required
def get_notifications():
    notifications = current_user.notifaction_data
    return jsonify(notifications)

@main.route('/mark_as_read', methods=['POST'])
@login_required
@email_verified_required
def mark_as_read():
    data = request.get_json()
    notification = data.get('notif')
    if notification not in current_user.notifaction_data['read']:
        current_user.notifaction_data['read'].append(notification)
        flag_modified(current_user, "notifaction_data")
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})

@main.route('/mark_all_as_read', methods=['POST'])
@login_required
@email_verified_required
def mark_all_as_read():
    current_user.notifaction_data['read'] = list(
        set(current_user.notifaction_data['read']) | set(current_user.notifaction_data['unread'])
    )
    current_user.notifaction_data['unread'] = []
    flag_modified(current_user, "notifaction_data")
    db.session.commit()
    return jsonify({"success": True})

# Add other notification-related routes here
