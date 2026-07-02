"""Recurring task API routes"""

import sys
from pathlib import Path
from flask import Blueprint, request, jsonify

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pmo import recurring

bp = Blueprint('recurring', __name__, url_prefix='/api/recurring')


@bp.route('', methods=['GET'])
def list_recurring():
    """List recurring task templates"""
    result = recurring.list_recurring()
    return jsonify(result)


@bp.route('', methods=['POST'])
def create_recurring():
    """Create a new recurring task template"""
    data = request.get_json()
    if not data or 'title' not in data or 'schedule_type' not in data:
        return jsonify({"error": "title and schedule_type required"}), 400

    tmpl = recurring.create_recurring(
        title=data['title'],
        schedule_type=data['schedule_type'],
        schedule_days=data.get('schedule_days'),
        priority=data.get('priority', 'medium'),
        description=data.get('description', '')
    )
    return jsonify(tmpl), 201


@bp.route('/<int:recurring_id>', methods=['PUT'])
def update_recurring(recurring_id):
    """Update a recurring task template"""
    data = request.get_json()
    tmpl = recurring.update_recurring(recurring_id, **data)
    if not tmpl:
        return jsonify({"error": "Recurring task not found"}), 404
    return jsonify(tmpl)


@bp.route('/<int:recurring_id>', methods=['DELETE'])
def delete_recurring(recurring_id):
    """Delete a recurring task template"""
    if recurring.delete_recurring(recurring_id):
        return '', 204
    return jsonify({"error": "Recurring task not found"}), 404
