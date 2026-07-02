import { useState, useEffect } from 'react';
import { api } from '../api/client';

export default function TaskForm({ task, date, onSave, onCancel }) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'medium',
    date: date,
  });

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title,
        description: task.description || '',
        priority: task.priority,
        date: task.date,
      });
    } else {
      setFormData({
        title: '',
        description: '',
        priority: 'medium',
        date: date,
      });
    }
  }, [task, date]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (task) {
        await api.updateTask(task.id, formData);
      } else {
        await api.createTask(formData);
      }
      onSave();
    } catch (err) {
      alert('Error saving task: ' + err.message);
    }
  };

  const handleDelete = async () => {
    if (!task) return;
    if (confirm('Delete this task?')) {
      try {
        await api.deleteTask(task.id);
        onSave();
      } catch (err) {
        alert('Error deleting task: ' + err.message);
      }
    }
  };

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h3>{task ? 'Edit Task' : 'New Task'}</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Title *</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              required
              autoFocus
            />
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows="3"
            />
          </div>

          <div className="form-group">
            <label>Priority</label>
            <select
              value={formData.priority}
              onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
            >
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>

          <div className="form-group">
            <label>Date</label>
            <input
              type="date"
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              required
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-primary">
              {task ? 'Save' : 'Create'}
            </button>
            {task && (
              <button type="button" className="btn-danger" onClick={handleDelete}>
                Delete
              </button>
            )}
            <button type="button" className="btn-secondary" onClick={onCancel}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
