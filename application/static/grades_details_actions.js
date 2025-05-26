API_URI = "/grades/"

function enableEditGrade(button) {
    const row = button.closest('tr');
    const cells = row.querySelectorAll('td');

    const typeValue = cells[3].innerText;
    const selectOptions = [
        'Sprawdzian',
        'Kartkówka',
        'Odpowiedź ustna'
    ];

    let selectHtml = '<select required>';
    selectOptions.forEach(option => {
        const selected = option === typeValue ? 'selected' : '';
        selectHtml += `<option value="${option}" ${selected}>${option}</option>`;
    });
    selectHtml += '</select>';
    cells[3].innerHTML = selectHtml;

    const gradeValue = cells[4].innerText;
    cells[4].innerHTML = `<input type="text" value="${gradeValue}">`;

    button.innerText = 'Zapisz';
    button.onclick = () => editGradeInDb(row, button);
}

function editGradeInDb(row, button) {
    const cells = row.querySelectorAll('td');
    const id = cells[2].innerText;
    const type = cells[3].querySelector('select').value;
    const value = cells[4].querySelector('input').value;

    const validValues = [1, 2, 3, 4, 5, 6]
    if (!validValues.includes(parseInt(value))) {
        alert("Wartość oceny jest niepoprawna")
        return
    }

    fetch(API_URI + 'update', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: id,
            type: type,
            value: value
        })
    }).then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            if (data.message) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Błąd przy edytowaniu oceny:', error);
        });
}

function deleteGradeFromDb(button) {
    const row = button.closest('tr');
    const cell = row.querySelectorAll('td');
    const id = cell[2].innerText

    fetch(API_URI + 'delete', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id: id})
    }).then(response => {
        if (!response.ok) {
            throw new Error("Błąd serwera");
        }
        return response.json();
    }).then(data => {
        alert("Ocena został usunięty.");
        location.reload();
    }).catch(error => {
        console.error('Błąd:', error);
        alert("Nie udało się usunąć oceny.");
    });
}