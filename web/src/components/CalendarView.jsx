import { useState, useEffect } from 'react';
import { api } from '../api/client';

export default function CalendarView({ date, tasks }) {
  const [timeBlocks, setTimeBlocks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTimeBlocks();
  }, [date]);

  const fetchTimeBlocks = async () => {
    try {
      setLoading(true);
      const blocks = await api.getTimeBlocks(date);
      setTimeBlocks(blocks);
    } catch (err) {
      console.error('Error fetching time blocks:', err);
    } finally {
      setLoading(false);
    }
  };

  const getTaskById = (taskId) => {
    return tasks.find(t => t.id === taskId);
  };

  const formatTime = (time) => {
    const [hours, minutes] = time.split(':');
    const h = parseInt(hours);
    const ampm = h >= 12 ? 'PM' : 'AM';
    const hour12 = h % 12 || 12;
    return `${hour12}:${minutes} ${ampm}`;
  };

  if (loading) {
    return (
      <div className="calendar-view">
        <h3>Calendar</h3>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="calendar-view">
      <h3>Calendar</h3>

      {timeBlocks.length === 0 ? (
        <div className="empty-state">
          <p>No appointments scheduled</p>
          <p className="hint">Use /add-timeblock to schedule tasks</p>
        </div>
      ) : (
        <div className="time-blocks">
          {timeBlocks.map(block => {
            const task = block.task_id ? getTaskById(block.task_id) : null;
            return (
              <div key={block.id} className="time-block-card">
                <div className="time-block-time">
                  {formatTime(block.start_time)} - {formatTime(block.end_time)}
                </div>
                <div className="time-block-content">
                  {task ? (
                    <>
                      <div className="time-block-title">{task.title}</div>
                      {task.description && (
                        <div className="time-block-desc">{task.description}</div>
                      )}
                      <span className={`time-block-priority ${task.priority}`}>
                        {task.priority}
                      </span>
                    </>
                  ) : (
                    <div className="time-block-title">{block.label}</div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
