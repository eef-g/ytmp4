const BASE = "/api";

export async function submitUrl(url) {
  const res = await fetch(`${BASE}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || JSON.stringify(err));
  }
  return res.json();
}

export async function fetchJobs() {
  const res = await fetch(`${BASE}/jobs`);
  if (!res.ok) throw new Error("Failed to fetch jobs");
  return res.json();
}

export function downloadUrl(jobId) {
  return `${BASE}/jobs/${jobId}/download`;
}
