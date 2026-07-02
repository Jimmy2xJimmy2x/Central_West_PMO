import PriorityBadge from './PriorityBadge';
import { api } from '../api/client';

export default function TaskCard({ task, onUpdate, onEdit }) {
  const handleToggle = async (e) => {
    if (e.target.tagName === 'INPUT') {
      const newStatus = task.status === 'done' ? 'pending' : 'done';
      await api.updateTask(task.id, { status: newStatus });
      onUpdate();
    }
  };

  const handleClick = (e) => {
    if (e.target.tagName === 'INPUT') return;
    onEdit(task);
  };

  return (
    <div className={`task-card ${task.status}`}>
      <div onClick={handleClick} style={{ cursor: 'pointer' }}>
        <input
          type="checkbox"
          checked={task.status === 'done'}
          onChange={handleToggle}
          onClick={(e) => e.stopPropagation()}
          style={{ marginRight: '8px', cursor: 'pointer' }}
        />
        <PriorityBadge priority={task.priority} />
        <span className="task-title" style={{ marginLeft: '8px' }}>
          {task.title}
        </span>
        {task.recurring_id && <span style={{ marginLeft: '8px' }}>↻</span>}
      </div>
      {task.description && (
        <div style={{ marginTop: '8px', fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>
          {task.description}
        </div>
      )}
    </div>
  );
}
