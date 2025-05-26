const date = document.body.dataset.date;
API_URI = `/attendance/${date}/`

function enableEditAttendance(button) {
    const row = button.closest('tr');
    const cells = row.querySelectorAll('td');

    const typeValue = cells[3].innerText.trim();
    const selectOptions = [
        'obecny',
        'niobecny',
        'spóźniony',
        'usprawiedliwiony'
    ];
    let selectHtml = `<select>`;
    selectOptions.forEach(option => {
        const selected = option === typeValue ? 'selected' : '';
        selectHtml += `<option value="${option}" ${selected}>${option}</option>`;
    });
    selectHtml += '</select>';
    cells[3].innerHTML = selectHtml;


    button.innerText = 'Zapisz';
    button.onclick = () => editAttendanceInDb(row);
}
function editAttendanceInDb(row) {
    const cells = row.querySelectorAll('td');
    const attendance_id = cells[0].innerText.trim();
    const attendance_name = cells[3].querySelector('select').value;

    fetch(API_URI + 'update',{
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: parseInt(attendance_id),
            status :  attendance_name,
        })
    }).then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Odpowiedź z backendu:", data);
        if (data.message) {
            alert(data.message);
            location.reload();
        } else if (data.error) {
            alert('Błąd: ' + data.error);
        } else {
            alert('Nieznany błąd');
        }
    })
    .catch(error => {
        console.error('Błąd przy edytowaniu obecności', error);
        alert('Błąd połączenia z serwerem: ' + error.message);
    });
}