import { useState } from 'react';
import './styles/app.css';
import DaySelector from './components/DaySelector';
import TaskList from './components/TaskList';
import TaskForm from './components/TaskForm';
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
        <h1>Central West PMO</h1>
        <button onClick={handleNewTask} className="btn-primary">
          + New Task
        </button>
      </header>
      <main className="main">
        <DaySelector selectedDate={selectedDate} onDateChange={setSelectedDate} />

        {loading && <p>Loading tasks...</p>}
        {error && <p style={{ color: 'var(--color-priority-high)' }}>Error: {error}</p>}
        {!loading && !error && <TaskList tasks={tasks} onUpdate={refetch} onEdit={handleEditTask} />}
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
