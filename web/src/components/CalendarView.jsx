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

  const formatDate = (dateStr) => {
    const date = new Date(dateStr + 'T00:00:00');
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    });
  };

  const getMeetingPlatform = (url) => {
    if (!url) return null;
    if (url.includes('meet.google.com')) return 'Google Meet';
    if (url.includes('zoom.us')) return 'Zoom';
    if (url.includes('teams.microsoft.com')) return 'Microsoft Teams';
    if (url.includes('webex.com')) return 'Webex';
    return 'Meeting Link';
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
            const title = task ? task.title : block.label;
            const meetingPlatform = getMeetingPlatform(block.meeting_link);

            return (
              <div key={block.id} className="appointment-card">
                <div className="appointment-header">
                  <div className="appointment-title">{title}</div>
                  {task && (
                    <span className={`appointment-priority ${task.priority}`}>
                      {task.priority}
                    </span>
                  )}
                </div>

                <div className="appointment-time">
                  🕐 {formatTime(block.start_time)} - {formatTime(block.end_time)}
                </div>

                <div className="appointment-date">
                  📅 {formatDate(block.date)}
                </div>

                {task?.description && (
                  <div className="appointment-desc">{task.description}</div>
                )}

                {block.meeting_link && (
                  <a
                    href={block.meeting_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="meeting-link"
                  >
                    🔗 {meetingPlatform}
                  </a>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
