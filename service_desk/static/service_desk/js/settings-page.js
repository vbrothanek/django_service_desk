/**
 * Toggles the visibility of the central email addresses field
 * based on the state of the central notification switch.
 * The field is hidden when the switch is unchecked and visible when checked.
 */

document.addEventListener('DOMContentLoaded', () => {
    const centralEmailsSwitcher = document.getElementById('central-emails-switcher');
    const centralEmailsField = document.getElementById('settings-emails-filed');

    centralEmailsSwitcher.addEventListener('click', (e) => {
        centralEmailsField.hidden = !e.target.checked;
        console.log(centralEmailsField.hidden);
    })
})