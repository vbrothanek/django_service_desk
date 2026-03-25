/**
 * Initializes TomSelect on company select fields and sets up dynamic requester loading.
 * When a company is selected, fetches the list of users belonging to that company
 * via an API call and populates the requester select field.
 *
 * @listens change - Fires when the company selection changes
 * @param {string} value - The selected company ID
 */
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('select.tom-select-company').forEach(select => {
        const ts = new TomSelect(select, {
            allowEmptyOption: true,
            placeholder: 'Select company...',
            items: [],
        });

        ts.on('change', (value) => {
            console.log(value);
            if (!value) {
                return;
            }

            const url = `/api/company/${value}/requesters/`

            const requesterEl = document.querySelector('select.tom-select-requester');
            if (requesterEl && requesterEl.tomselect) {
                requesterEl.tomselect.destroy();
            }

            /**
             * Destroys the existing TomSelect instance on the requester field,
             * fetches requester options for the selected company from the API,
             * injects the returned HTML options into the requester select field,
             * removes the disabled attribute and re-initializes TomSelect.
             *
             * @param {string} url - The API endpoint URL for fetching company requesters
             * @param {HTMLElement} requesterEl - The requester select element
             */

            htmx.ajax('GET', url, {
                target: '#id_requester',
                swap: 'innerHTML'
            }).then(() => {
                requesterEl.removeAttribute('disabled');
                new TomSelect(requesterEl, {
                    allowEmptyOption: true,
                    controlInput: null
                });
            })
        })
    })

    document.querySelectorAll('select.tom-select-company-ticket-detail').forEach(select => {
        const ts = new TomSelect(select, {
            allowEmptyOption: true,
        });

        ts.on('change', (value) => {
            console.log(value);
            if (!value) {
                return;
            }

            const url = `/api/company/${value}/requesters/`

            const requesterEl = document.querySelector('select.tom-select-requester');
            if (requesterEl && requesterEl.tomselect) {
                requesterEl.tomselect.destroy();
            }

            /**
             * Destroys the existing TomSelect instance on the requester field,
             * fetches requester options for the selected company from the API,
             * injects the returned HTML options into the requester select field,
             * removes the disabled attribute and re-initializes TomSelect.
             *
             * @param {string} url - The API endpoint URL for fetching company requesters
             * @param {HTMLElement} requesterEl - The requester select element
             */

            htmx.ajax('GET', url, {
                target: '#id_requester',
                swap: 'innerHTML'
            }).then(() => {
                requesterEl.removeAttribute('disabled');
                new TomSelect(requesterEl, {
                    allowEmptyOption: true,
                    controlInput: null
                });
            })
        })
    })

    document.querySelectorAll('select.tom-select-priority').forEach(select => {
        new TomSelect(select, {
            controlInput: null,
        })
    })

    document.querySelectorAll('select.tom-select-status-ticket-detail').forEach(select => {
        new TomSelect(select, {
            allowEmptyOption: false,
            controlInput: null,
        })
    })

    document.querySelectorAll('select.tom-select-followers').forEach(select => {
        new TomSelect(select, {
            allowEmptyOption: true,
            plugins: ['remove_button'],
            hideSelected: true,
        })
    })

    document.querySelectorAll('select.tom-select-assigned-ticket-detail').forEach(select => {
        new TomSelect(select, {
            allowEmptyOption: false,
            maxItems: 1,
            // controlInput: null,
            placeholder: 'Select assignee...',
        })
    })

    document.querySelectorAll('select.tom-select-filter-status').forEach(select => {
        new TomSelect(select, {
            allowEmptyOption: true,
            plugins: ['remove_button'],
            controlInput: null,
        })
    })

    document.querySelectorAll('select.tom-select-filter-priority').forEach(select => {
        new TomSelect(select, {
            allowEmptyOption: true,
            plugins: ['remove_button'],
            controlInput: null,
        })
    })

    document.querySelectorAll('select.tom-select-requester').forEach(select => {
        new TomSelect(select, {
            allowEmptyOption: true,
            controlInput: null,
        })
    })
})

