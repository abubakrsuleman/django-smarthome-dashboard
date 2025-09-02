(function () {
  function updateClock() {
    var clockEl = document.getElementById("clock");
    var dateEl  = document.getElementById("dateLine");
    if (!clockEl || !dateEl) return; // elements not on this page

    var now = new Date();

    try {
      clockEl.textContent = now.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false
      });
    } catch (e) {
      // Very old browsers fallback
      clockEl.textContent = now.getHours().toString().padStart(2,"0") + ":" +
                            now.getMinutes().toString().padStart(2,"0") + ":" +
                            now.getSeconds().toString().padStart(2,"0");
    }

    try {
      dateEl.textContent = now.toLocaleDateString(undefined, {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric"
      });
    } catch (e) {
      dateEl.textContent = now.toDateString();
    }
  }

  function startClock() {
    updateClock();
    setInterval(updateClock, 1000);
  }

  // Ensure DOM is ready before trying to find #clock / #dateLine
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startClock);
  } else {
    startClock();
  }
})();

