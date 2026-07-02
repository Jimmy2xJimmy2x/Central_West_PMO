"""Task notes API routes"""

import sys
from pathlib import Path
from flask import Blueprint, request, jsonify

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pmo import notes as notes_module

bp = Blueprint('notes', __name__, url_prefix='/api')


@bp.route('/tasks/<int:task_id>/notes', methods=['GET'])
def list_notes(task_id):
    """List notes for a task"""
    result = notes_module.list_notes(task_id)
    return jsonify(result)


@bp.route('/tasks/<int:task_id>/notes', methods=['POST'])
def add_note(task_id):
    """Add a note to a task"""
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "content required"}), 400

    note = notes_module.add_note(
        task_id=task_id,
        content=data['content'],
        note_type=data.get('note_type', 'text')
    )
    return jsonify(note), 201


@bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a note"""
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "content required"}), 400

    note = notes_module.update_note(note_id, data['content'])
    if not note:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(note)


@bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note"""
    if notes_module.delete_note(note_id):
        return '', 204
    return jsonify({"error": "Note not found"}), 404
