function formatBytes(bytes) {
  if (!bytes) return "0 B";
  const sizes = ["B", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return (bytes / Math.pow(1024, i)).toFixed(1) + " " + sizes[i];
}

async function updateSystemStatus() {
  try {
    const res = await fetch("/data/system-status/");
    const data = await res.json();

    document.getElementById("cpu").textContent = data.cpu + "%";
    document.getElementById("mem").textContent = data.memory.percent + "%";
    document.getElementById("memBytes").textContent =
      formatBytes(data.memory.used) + " / " + formatBytes(data.memory.total);
    document.getElementById("disk").textContent = data.disk.percent + "%";
    document.getElementById("diskBytes").textContent =
      formatBytes(data.disk.used) + " / " + formatBytes(data.disk.total);
  } catch (err) {
    console.error("Failed to fetch system status", err);
  }
}

setInterval(updateSystemStatus, 5000); // update every 5 seconds
updateSystemStatus();
