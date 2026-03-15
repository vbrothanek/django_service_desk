// Edit modal — open after HTMX loads content
document.addEventListener('htmx:afterSwap', function (e) {
    if (e.detail.target.id === 'record-edit-modal-content') {
        new bootstrap.Modal(document.getElementById('record-edit-modal')).show();
    }
});

// Delete modal — set form action and open
document.addEventListener('click', function (e) {
    const btn = e.target.closest('[data-delete-url]');
    if (btn) {
        document.getElementById('record-delete-form').action = btn.dataset.deleteUrl;
        new bootstrap.Modal(document.getElementById('record-delete-modal')).show();
    }
});

// Expand all toggle
document.getElementById('toggle-records')?.addEventListener('change', function () {
    document.querySelectorAll('[id^="record-"]').forEach(el => {
        el.style.whiteSpace = this.checked ? 'normal' : 'nowrap';
    });
})


const toggleRecords = document.getElementById('toggle-records');

// Restore saved state
if (toggleRecords) {
    const saved = localStorage.getItem('recordsExpanded') === 'true';
    toggleRecords.checked = saved;
    document.querySelectorAll('[id^="record-"]').forEach(el => {
        el.style.whiteSpace = saved ? 'normal' : 'nowrap';
    });

    toggleRecords.addEventListener('change', function () {
        localStorage.setItem('recordsExpanded', this.checked);
        document.querySelectorAll('[id^="record-"]').forEach(el => {
            el.style.whiteSpace = this.checked ? 'normal' : 'nowrap';
        });
    });
}