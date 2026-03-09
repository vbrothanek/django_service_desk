// Initialization of tom select
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('select.tom-select-company').forEach(select => {
        new TomSelect(select, {
            allowEmptyOption: true,
            placeholder: 'Select company...',
            items: [],
        })
    })

    document.querySelectorAll('select.tom-select-company-ticket-detail').forEach(select => {
        new TomSelect(select, {
            allowEmptyOption: true,
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
            controlInput: null,
        })
    })

    document.querySelectorAll('select.tom-select-filter-priority').forEach(select => {
        new TomSelect(select, {
            allowEmptyOption: true,
            controlInput: null,
        })
    })
})

