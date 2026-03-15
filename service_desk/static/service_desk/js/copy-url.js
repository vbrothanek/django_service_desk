function copyUrl(el) {
    navigator.clipboard.writeText(window.location.href);
    const toast = document.getElementById('copy-notification');
    toast.classList.remove('animate');
    void toast.offsetWidth; // force reflow
    toast.classList.add('animate');
}