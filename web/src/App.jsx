import { useState } from 'react';
import './styles/app.css';
import DaySelector from './components/DaySelector';
import TaskList from './components/TaskList';
import { useTasks } from './hooks/useTasks';
import { getTodayISO } from './utils/dates';

function App() {
  const [selectedDate, setSelectedDate] = useState(getTodayISO());
  const { tasks, loading, error, refetch } = useTasks(selectedDate);

  return (
    <div className="app">
      <header className="header">
        <h1>Central West PMO</h1>
      </header>
      <main className="main">
        <DaySelector selectedDate={selectedDate} onDateChange={setSelectedDate} />

        {loading && <p>Loading tasks...</p>}
        {error && <p style={{ color: 'var(--color-priority-high)' }}>Error: {error}</p>}
        {!loading && !error && <TaskList tasks={tasks} onUpdate={refetch} />}
      </main>
    </div>
  );
}

export default App;
