<script>
  import { submitUrl } from "../lib/api.js";
  import { addError } from "../lib/stores.js";

  let url = $state("");
  let loading = $state(false);

  const VALID_PATTERN =
    /^https?:\/\/(www\.)?(youtube\.com|youtu\.be|instagram\.com|tiktok\.com|vm\.tiktok\.com)/i;

  async function handleSubmit() {
    const trimmed = url.trim();
    if (!trimmed) return;

    if (!VALID_PATTERN.test(trimmed)) {
      addError("Invalid URL. Supported: YouTube, Instagram, TikTok");
      return;
    }

    loading = true;
    try {
      await submitUrl(trimmed);
      url = "";
    } catch (e) {
      addError(e.message);
    } finally {
      loading = false;
    }
  }
</script>

<form class="url-input" onsubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
  <input
    type="url"
    bind:value={url}
    placeholder="Paste a YouTube, Instagram, or TikTok link..."
    disabled={loading}
  />
  <button type="submit" disabled={loading || !url.trim()}>
    {loading ? "Submitting..." : "Download"}
  </button>
</form>

<style>
  .url-input {
    display: flex;
    gap: 0.75rem;
    max-width: 700px;
    margin: 0 auto;
  }

  input {
    flex: 1;
    padding: 0.85rem 1.1rem;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    font-size: 1rem;
    outline: none;
    transition: border-color 0.2s;
  }

  input:focus {
    border-color: var(--accent);
  }

  input::placeholder {
    color: var(--text-muted);
  }

  button {
    padding: 0.85rem 1.5rem;
    border-radius: var(--radius);
    background: var(--accent);
    color: white;
    font-weight: 600;
    font-size: 1rem;
    transition: background 0.2s;
  }

  button:hover:not(:disabled) {
    background: var(--accent-hover);
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
