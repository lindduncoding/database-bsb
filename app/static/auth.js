document.body.addEventListener("htmx:configRequest", function (event) {
    const token = localStorage.getItem("access_token");
    if (token) {
        event.detail.headers["Authorization"] = `Bearer ${token}`;
    }
})
