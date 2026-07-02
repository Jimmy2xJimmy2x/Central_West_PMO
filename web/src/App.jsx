import { useState } from 'react';
import './styles/app.css';
import DaySelector from './components/DaySelector';
import TaskList from './components/TaskList';
import TaskForm from './components/TaskForm';
import CalendarView from './components/CalendarView';
import { useTasks } from './hooks/useTasks';
import { getTodayISO } from './utils/dates';

function App() {
  const [selectedDate, setSelectedDate] = useState(getTodayISO());
  const { tasks, loading, error, refetch } = useTasks(selectedDate);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  const handleNewTask = () => {
    setEditingTask(null);
    setShowForm(true);
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleFormClose = () => {
    setShowForm(false);
    setEditingTask(null);
    refetch();
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-left">
          <img src="/redhat-logo.svg" alt="Red Hat" className="redhat-logo" />
          <h1>Central West PMO</h1>
        </div>
        <button onClick={handleNewTask} className="btn-primary">
          + New Task
        </button>
      </header>
      <main className="main">
        <DaySelector selectedDate={selectedDate} onDateChange={setSelectedDate} />

        {loading && <p>Loading tasks...</p>}
        {error && <p style={{ color: 'var(--color-priority-high)' }}>Error: {error}</p>}
        {!loading && !error && (
          <div className="two-column-layout">
            <div className="tasks-column">
              <h3>Tasks</h3>
              <TaskList tasks={tasks} onUpdate={refetch} onEdit={handleEditTask} />
            </div>
            <div className="calendar-column">
              <CalendarView date={selectedDate} tasks={tasks} />
            </div>
          </div>
        )}
      </main>

      {showForm && (
        <TaskForm
          task={editingTask}
          date={selectedDate}
          onSave={handleFormClose}
          onCancel={() => setShowForm(false)}
        />
      )}
    </div>
  );
}

export default App;
