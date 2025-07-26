document.addEventListener("DOMContentLoaded", function() {
    const token = localStorage.getItem("access_token");
    if (!token) {
    window.location.href = "/"
    return
    }
})

document.addEventListener("htmx:configRequest", function (event) {
    const token = localStorage.getItem("access_token");
    if (token) {
        event.detail.headers["Authorization"] = `Bearer ${token}`;
    }
})