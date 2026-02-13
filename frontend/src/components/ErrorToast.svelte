<script>
  import { errors, dismissError } from "../lib/stores.js";
</script>

{#if $errors.length > 0}
  <div class="toast-container">
    {#each $errors as err (err.id)}
      <div class="toast">
        <span>{err.message}</span>
        <button onclick={() => dismissError(err.id)}>&times;</button>
      </div>
    {/each}
  </div>
{/if}

<style>
  .toast-container {
    position: fixed;
    top: 1.5rem;
    right: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    z-index: 1000;
    max-width: 400px;
  }

  .toast {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.85rem 1rem;
    background: var(--error);
    color: white;
    border-radius: var(--radius);
    font-size: 0.9rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    animation: slideIn 0.25s ease;
  }

  .toast span {
    flex: 1;
    word-break: break-word;
  }

  .toast button {
    background: none;
    color: white;
    font-size: 1.3rem;
    line-height: 1;
    padding: 0 0.25rem;
    opacity: 0.8;
  }

  .toast button:hover {
    opacity: 1;
  }

  @keyframes slideIn {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
</style>
