async function createLink() {
  const apiKey = document.getElementById("apiKey").value.trim();
  const url = document.getElementById("urlInput").value.trim();

  if (!apiKey || !url) {
    alert("Missing API key or URL");
    return;
  }

  const res = await fetch("/api/links/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-ADMIN-TOKEN": apiKey,
    },
    body: JSON.stringify({ url }),
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.error || "Error creating link");
    return;
  }

  document.getElementById("shortUrl").value = data.short_url;
  document.getElementById("result").style.display = "block";
}

function copyToClipboard() {
  const input = document.getElementById("shortUrl");

  navigator.clipboard.writeText(input.value).then(() => {
    document.getElementById("status").innerText = "Copied!";
  }).catch(() => {
    document.getElementById("status").innerText = "Copy failed";
  });
}

function toggleKey() {
  const input = document.getElementById("apiKey");
  input.type = input.type === "password" ? "text" : "password";
}