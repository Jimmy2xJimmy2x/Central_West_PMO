const BASE = '/api';

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(error.error || res.statusText);
  }
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  // Tasks
  getTasks: (date) => request(`/tasks?date=${date}`),
  createTask: (data) => request('/tasks', { method: 'POST', body: data }),
  updateTask: (id, data) => request(`/tasks/${id}`, { method: 'PUT', body: data }),
  deleteTask: (id) => request(`/tasks/${id}`, { method: 'DELETE' }),

  // Time blocks
  getTimeBlocks: (date) => request(`/timeblocks?date=${date}`),
  createTimeBlock: (data) => request('/timeblocks', { method: 'POST', body: data }),
  updateTimeBlock: (id, data) => request(`/timeblocks/${id}`, { method: 'PUT', body: data }),
  deleteTimeBlock: (id) => request(`/timeblocks/${id}`, { method: 'DELETE' }),

  // Recurring
  getRecurring: () => request('/recurring'),
  createRecurring: (data) => request('/recurring', { method: 'POST', body: data }),
  updateRecurring: (id, data) => request(`/recurring/${id}`, { method: 'PUT', body: data }),
  deleteRecurring: (id) => request(`/recurring/${id}`, { method: 'DELETE' }),

  // Notes
  getNotes: (taskId) => request(`/tasks/${taskId}/notes`),
  addNote: (taskId, data) => request(`/tasks/${taskId}/notes`, { method: 'POST', body: data }),
  updateNote: (id, data) => request(`/notes/${id}`, { method: 'PUT', body: data }),
  deleteNote: (id) => request(`/notes/${id}`, { method: 'DELETE' }),
};
