document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("emailForm");
    const loadingIndicator = document.getElementById("loading");
    const toast = document.getElementById("toast");

    function showToast(message, success = true) {
        toast.innerText = message;
        toast.className = success ? "toast success show" : "toast error show";

        setTimeout(() => {
            toast.classList.remove("show");
        }, 3000);
    }

    if (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            const email = document.getElementById("email").value;
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!emailPattern.test(email)) {
                showToast("Invalid email address", false);
                return;
            }

            loadingIndicator.style.display = "block";

            fetch(`/send_phishing_email/${encodeURIComponent(email)}`)
                .then(res => res.text())
                .then(data => {
                    loadingIndicator.style.display = "none";
                    showToast(data, true);
                    form.reset();
                })
                .catch(() => {
                    loadingIndicator.style.display = "none";
                    showToast("Failed to send email", false);
                });
        });
    }
});