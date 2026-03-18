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
        el.style.whiteSpace = this.checked ? 'pre-wrap' : 'nowrap';
    });
})


const toggleRecords = document.getElementById('toggle-records');

// Restore saved state
if (toggleRecords) {
    const saved = localStorage.getItem('recordsExpanded') === 'true';
    toggleRecords.checked = saved;
    document.querySelectorAll('.record-message').forEach(el => {
        el.style.whiteSpace = saved ? 'pre-wrap' : 'nowrap';
    });

    toggleRecords.addEventListener('change', function () {
        localStorage.setItem('recordsExpanded', this.checked);
        document.querySelectorAll('.record-message').forEach(el => {
            el.style.whiteSpace = this.checked ? 'pre-wrap' : 'nowrap';
        });
    });
}


// Set correct height of modal in record edit
document.addEventListener('htmx:afterSwap', function (e) {
    if (e.detail.target.id === 'record-edit-modal-content') {
        const modalEl = document.getElementById('record-edit-modal');
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();

        modalEl.addEventListener('shown.bs.modal', function () {
            const textarea = modalEl.querySelector('textarea');
            if (textarea) {
                textarea.style.height = 'auto';
                textarea.style.height = textarea.scrollHeight + 'px';
            }
        }, {once: true});
    }
});

