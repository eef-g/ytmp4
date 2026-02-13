<script>
  import { jobs } from "../lib/stores.js";
  import JobItem from "./JobItem.svelte";

  let jobList = $derived(
    Object.values($jobs).sort((a, b) => {
      // Show newest first (by job_id which is based on creation order)
      return a.job_id > b.job_id ? -1 : 1;
    })
  );
</script>

{#if jobList.length > 0}
  <div class="job-list">
    {#each jobList as job (job.job_id)}
      <JobItem {job} />
    {/each}
  </div>
{/if}

<style>
  .job-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-width: 700px;
    margin: 0 auto;
  }
</style>
