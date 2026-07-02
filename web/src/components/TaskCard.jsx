import PriorityBadge from './PriorityBadge';
import { api } from '../api/client';

export default function TaskCard({ task, onUpdate }) {
  const handleToggle = async () => {
    const newStatus = task.status === 'done' ? 'pending' : 'done';
    await api.updateTask(task.id, { status: newStatus });
    onUpdate();
  };

  return (
    <div className={`task-card ${task.status}`} onClick={handleToggle}>
      <div>
        <input
          type="checkbox"
          checked={task.status === 'done'}
          onChange={() => {}}
          style={{ marginRight: '8px' }}
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
