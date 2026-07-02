"""Time block API routes"""

import sys
from pathlib import Path
from flask import Blueprint, request, jsonify

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pmo import timeblocks as tb_module

bp = Blueprint('timeblocks', __name__, url_prefix='/api/timeblocks')


@bp.route('', methods=['GET'])
def list_timeblocks():
    """List time blocks for a date"""
    date = request.args.get('date')
    if not date:
        return jsonify({"error": "date parameter required"}), 400

    result = tb_module.list_timeblocks(date)
    return jsonify(result)


@bp.route('', methods=['POST'])
def create_timeblock():
    """Create a new time block"""
    data = request.get_json()
    if not data or 'date' not in data or 'start_time' not in data or 'end_time' not in data:
        return jsonify({"error": "date, start_time, and end_time required"}), 400

    block = tb_module.create_timeblock(
        date=data['date'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        task_id=data.get('task_id'),
        label=data.get('label', '')
    )
    return jsonify(block), 201


@bp.route('/<int:block_id>', methods=['PUT'])
def update_timeblock(block_id):
    """Update a time block"""
    data = request.get_json()
    block = tb_module.update_timeblock(block_id, **data)
    if not block:
        return jsonify({"error": "Time block not found"}), 404
    return jsonify(block)


@bp.route('/<int:block_id>', methods=['DELETE'])
def delete_timeblock(block_id):
    """Delete a time block"""
    if tb_module.delete_timeblock(block_id):
        return '', 204
    return jsonify({"error": "Time block not found"}), 404
