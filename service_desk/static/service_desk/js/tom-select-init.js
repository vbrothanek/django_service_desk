// Initialization of tom select
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('select.tom-select-company').forEach(select => {
        new TomSelect(select, {
            allowEmptyOption: true,
            // plugins: ['remove_button'],
            placeholder: 'Select company...',
            items: [],
        })
    })

    document.querySelectorAll('select.tom-select-priority').forEach(select => {
    new TomSelect(select, {
        controlInput: null,
        })
    })
})