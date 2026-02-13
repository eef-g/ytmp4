<script>
  import { downloadUrl } from "../lib/api.js";

  let { job } = $props();

  const statusLabels = {
    pending: "Queued",
    downloading: "Downloading",
    processing: "Processing",
    done: "Done",
    error: "Failed",
  };
</script>

<div class="job-item" class:error={job.status === "error"} class:done={job.status === "done"}>
  <div class="job-header">
    <span class="job-title">{job.title || job.url}</span>
    <span class="badge" class:badge-done={job.status === "done"} class:badge-error={job.status === "error"}>
      {statusLabels[job.status] || job.status}
    </span>
  </div>

  {#if job.status === "downloading" || job.status === "processing"}
    <div class="progress-bar">
      <div class="progress-fill" style="width: {job.progress}%"></div>
    </div>
    <span class="progress-text">{job.progress}%</span>
  {/if}

  {#if job.status === "error"}
    <p class="error-text">{job.error}</p>
  {/if}

  {#if job.status === "done"}
    <a class="download-btn" href={downloadUrl(job.job_id)} download>
      Download MP4
    </a>
  {/if}
</div>

<style>
  .job-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
  }

  .job-item.done {
    border-color: var(--success);
  }

  .job-item.error {
    border-color: var(--error);
  }

  .job-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
  }

  .job-title {
    font-size: 0.95rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    min-width: 0;
  }

  .badge {
    flex-shrink: 0;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    background: var(--progress-bg);
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }

  .badge-done {
    background: rgba(34, 197, 94, 0.15);
    color: var(--success);
  }

  .badge-error {
    background: rgba(239, 68, 68, 0.15);
    color: var(--error);
  }

  .progress-bar {
    height: 6px;
    background: var(--progress-bg);
    border-radius: 3px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: var(--progress-fill);
    border-radius: 3px;
    transition: width 0.3s ease;
  }

  .progress-text {
    font-size: 0.8rem;
    color: var(--text-muted);
  }

  .error-text {
    font-size: 0.85rem;
    color: var(--error);
    word-break: break-word;
  }

  .download-btn {
    display: inline-block;
    align-self: flex-start;
    padding: 0.5rem 1.2rem;
    border-radius: var(--radius);
    background: var(--success);
    color: #fff;
    font-weight: 600;
    font-size: 0.9rem;
    text-decoration: none;
    transition: opacity 0.2s;
  }

  .download-btn:hover {
    opacity: 0.85;
  }
</style>
