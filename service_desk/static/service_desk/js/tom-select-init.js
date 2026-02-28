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
            allowEmptyOption: true,
        })
    })

    document.querySelectorAll('select.tom-select-followers').forEach(select => {
        new TomSelect(select, {
            allowEmptyOption: true,
            plugins: ['remove_button'],
            hideSelected: true,
        })
    })
})

