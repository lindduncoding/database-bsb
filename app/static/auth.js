function loginUser(event) {
  event.preventDefault();

  fetch("/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      username: document.querySelector("#username").value,
      password: document.querySelector("#password").value
    })
  })
  .then(r => r.json())
  .then(data => {
    if (data.access_token) {
      localStorage.setItem("access_token", data.access_token);

      // Load dashboard dynamically
      loadPage('/dashboard')
    } else {
      alert("Login failed")
    }
  })
}

function loadPage(url, targetId = null, expect = "auto") {
    const token = localStorage.getItem("access_token");

    fetch(url, {
        method: "GET",
        headers: {
            "Authorization": token ? `Bearer ${token}` : ""
        }
    })
    .then(async response => {
        const contentType = response.headers.get("content-type");
        const disposition = response.headers.get("content-disposition");

        if (disposition && disposition.includes("attachment")) {
            // It's a file download
            const blob = await response.blob();
            const urlObject = window.URL.createObjectURL(blob);

            // Extract filename
            let filename = "download";
            const match = disposition.match(/filename="?(.+)"?/);
            if (match && match[1]) filename = match[1];

            // Create temporary link
            const a = document.createElement("a");
            a.href = urlObject;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(urlObject);
            return;
        }

        if (contentType && contentType.includes("application/json")) {
            const data = await response.json();
            if (targetId) {
                document.getElementById(targetId).textContent = JSON.stringify(data, null, 2);
            } else {
                console.log("JSON Data:", data);
            }
        } else {
            const html = await response.text();
            if (targetId) {
                document.getElementById(targetId).innerHTML = html;
            } else {
                document.open();
                document.write(html);
                document.close();
            }
        }
    })
    .catch(err => console.error("Error loading page:", err));
}