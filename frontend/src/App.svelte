<script>
  import { onMount } from "svelte";
  import { loadJobs, connectSSE, disconnectSSE } from "./lib/stores.js";
  import UrlInput from "./components/UrlInput.svelte";
  import JobList from "./components/JobList.svelte";
  import ErrorToast from "./components/ErrorToast.svelte";

  onMount(() => {
    loadJobs();
    connectSSE();
    return () => disconnectSSE();
  });
</script>

<main>
  <header>
    <h1>ytmp4</h1>
    <p>Download videos from YouTube, Instagram & TikTok</p>
  </header>

  <section class="input-section">
    <UrlInput />
  </section>

  <section class="jobs-section">
    <JobList />
  </section>

  <ErrorToast />
</main>

<style>
  main {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
    min-height: 100vh;
  }

  header {
    text-align: center;
    margin-bottom: 2.5rem;
  }

  h1 {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, var(--accent), #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  header p {
    color: var(--text-muted);
    margin-top: 0.4rem;
    font-size: 1.05rem;
  }

  .input-section {
    margin-bottom: 2rem;
  }

  .jobs-section {
    margin-bottom: 2rem;
  }
</style>
