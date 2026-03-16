/*
   * Polls the server every 10 seconds to check for ticket updates.
   *
   * setInterval() repeatedly calls the async function every 10 000ms.
   *
   * Inside each call:
   * - fetch() sends a GET request to the poll endpoint and waits for the response
   * - .json() parses the response body as JSON and waits for the result
   * - On the first call, lastTs is null so we just store the current timestamp as baseline
   * - On subsequent calls, we compare the new timestamp with the stored one
   * - If they differ, a ticket was updated — we update lastTs and trigger a 'refresh' event
   *   on the container, which HTMX catches via hx-trigger="refresh" and reloads the table
   * - If they are the same, nothing happens — no reload, no extra DB queries
   */

const container = document.getElementById('tickets-container');
const pollUrl = container.dataset.pollUrl;

let lastTimeStamp = null;

setInterval(async () => {
    const response = await fetch(pollUrl);
    const data = await response.json();

    if (lastTimeStamp === null) {
        lastTimeStamp = data.ts;
    } else if (data.ts !== lastTimeStamp) {
        lastTimeStamp = data.ts;
        htmx.trigger(container, 'refresh')
    }
}, 10000)