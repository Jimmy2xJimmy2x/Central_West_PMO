import { useState, useEffect } from 'react';
import { api } from '../api/client';

export function useTasks(date) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const data = await api.getTasks(date);
      setTasks(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [date]);

  return { tasks, loading, error, refetch: fetchTasks };
}
