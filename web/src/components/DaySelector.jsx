import { formatDate, addDays } from '../utils/dates';

export default function DaySelector({ selectedDate, onDateChange }) {
  return (
    <div className="day-selector">
      <button onClick={() => onDateChange(addDays(selectedDate, -1))}>
        ← Prev
      </button>
      <h2>{formatDate(selectedDate)}</h2>
      <button onClick={() => onDateChange(addDays(selectedDate, 1))}>
        Next →
      </button>
    </div>
  );
}
