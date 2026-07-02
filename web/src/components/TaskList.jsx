import TaskCard from './TaskCard';

export default function TaskList({ tasks, onUpdate }) {
  // Group by priority
  const byPriority = {
    high: tasks.filter(t => t.priority === 'high'),
    medium: tasks.filter(t => t.priority === 'medium'),
    low: tasks.filter(t => t.priority === 'low'),
  };

  const doneCount = tasks.filter(t => t.status === 'done').length;

  return (
    <div>
      <div style={{ marginBottom: '16px', color: 'var(--color-text-muted)' }}>
        {doneCount}/{tasks.length} completed
      </div>
      <div className="task-list">
        {['high', 'medium', 'low'].map(priority =>
          byPriority[priority].map(task => (
            <TaskCard key={task.id} task={task} onUpdate={onUpdate} />
          ))
        )}
      </div>
    </div>
  );
}
