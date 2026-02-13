import { writable } from "svelte/store";
import { fetchJobs } from "./api.js";

export const jobs = writable({});
export const errors = writable([]);

let errorId = 0;

export function addError(message) {
  const id = ++errorId;
  errors.update((e) => [...e, { id, message }]);
  setTimeout(() => dismissError(id), 5000);
}

export function dismissError(id) {
  errors.update((e) => e.filter((err) => err.id !== id));
}

export async function loadJobs() {
  try {
    const list = await fetchJobs();
    const map = {};
    for (const job of list) {
      map[job.job_id] = job;
    }
    jobs.set(map);
  } catch {
    addError("Failed to load jobs");
  }
}

let eventSource = null;

export function connectSSE() {
  if (eventSource) eventSource.close();

  eventSource = new EventSource("/api/events");

  eventSource.addEventListener("job_update", (e) => {
    try {
      const job = JSON.parse(e.data);
      jobs.update((current) => ({ ...current, [job.job_id]: job }));
    } catch {
      // ignore parse errors
    }
  });

  eventSource.onerror = () => {
    // EventSource auto-reconnects
  };
}

export function disconnectSSE() {
  if (eventSource) {
    eventSource.close();
    eventSource = null;
  }
}
