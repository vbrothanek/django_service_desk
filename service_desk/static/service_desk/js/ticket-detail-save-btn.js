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
            console.log('chaged tom select')
            select.tomselect.on('change', () => {
                button.disabled = false;
            });
        }
    });
})


