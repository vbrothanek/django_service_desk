//Validating if change happened on the website.
// If there is a change activate button for save changes.

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#ticket-detail-form');
    const button = document.getElementById('save-button');

    form.addEventListener('input', event => {
        console.log("changed input")
        button.disabled =  false;
    });

    form.querySelectorAll('select').forEach(select => {
        if (select.tomselect) {
            select.tomselect.on('change', () => {
                button.disabled = false;
            });
        }
    });

    //Autosave function - after file is uploaded do submit automatically instead of saving form manually.
    const upload_file = document.getElementById('id_file');
    const upload_form = document.getElementById('attachment-upload-form');

    upload_file.addEventListener('change', () => {
        upload_form.submit();
    });
})


