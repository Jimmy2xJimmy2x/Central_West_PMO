"""Task API routes"""

import sys
from pathlib import Path
from flask import Blueprint, request, jsonify

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pmo import tasks as tasks_module, recurring

bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


@bp.route('', methods=['GET'])
def list_tasks():
    """List tasks for a date"""
    date = request.args.get('date')
    if not date:
        return jsonify({"error": "date parameter required"}), 400

    # Auto-generate recurring tasks
    recurring.generate_for_date(date)

    status = request.args.get('status')
    result = tasks_module.list_tasks(date, status)
    return jsonify(result)


@bp.route('', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()
    if not data or 'title' not in data or 'date' not in data:
        return jsonify({"error": "title and date required"}), 400

    task = tasks_module.create_task(
        title=data['title'],
        date=data['date'],
        priority=data.get('priority', 'medium'),
        description=data.get('description', ''),
        recurring_id=data.get('recurring_id')
    )
    return jsonify(task), 201


@bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task"""
    task = tasks_module.get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


@bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    data = request.get_json()
    task = tasks_module.update_task(task_id, **data)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


@bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    if tasks_module.delete_task(task_id):
        return '', 204
    return jsonify({"error": "Task not found"}), 404


@bp.route('/reorder', methods=['PUT'])
def reorder_tasks():
    """Reorder tasks for a date"""
    data = request.get_json()
    if not data or 'date' not in data or 'task_ids' not in data:
        return jsonify({"error": "date and task_ids required"}), 400

    tasks_module.reorder_tasks(data['date'], data['task_ids'])
    return '', 204
