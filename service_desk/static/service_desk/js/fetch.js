// fetch vrati promise -> prislib ze neco dostane
// then vola funkci - pak reaguje na dokonceny prislib s vyslekem

const btnFetch = document.getElementById('btn-fetch');

let dataUrl = '/api/'

btnFetch.addEventListener('click', event => {
    fetchData(dataUrl)
})


function fetchData() {
    fetch(dataUrl)
    .then(response => {
        return response.json();
    }).then(json => {
        const next = json.next
        console.log(next)

        const parent = document.getElementById('ticket-list-dashboard');

        if (json.next) {
            dataUrl = json.next;
        } else {
            btnFetch.setAttribute('disabled', '');
        }

        json.data.forEach(item => {
            const div = renderTicket(item);
            parent.appendChild(div);
        })


    });
}



function renderTicket(item) {
    const div = document.createElement('div');
    div.textContent = item.ticket_number + ' - ' + item.company__name;

    return div
}
