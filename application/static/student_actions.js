API_URI = "/students/"

function openGradeAddForm() {
    document.getElementById("grade-add-modal").style.display = "block";
}

function closeGradeAddForm() {
    document.getElementById("grade-add-modal").style.display = "none";
}

function openGradeDeleteForm() {
    document.getElementById("student-delete-modal").style.display = "block";
}

function closeGradeDeleteForm() {
    document.getElementById("student-delete-modal").style.display = "none";
}

function validateNameOrSurname(value) {
    const nameSurnameRegex = /^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\- ]+$/;
    return nameSurnameRegex.test(value.trim());
}

function validatePesel(value) {
    const peselRegex = /^\d{11}$/;
    return peselRegex.test(value);
}

function validateClassId(value) {
    const classIdRegex = /^\d+$/;
    return classIdRegex.test(value);
}


function addStudentToDb() {
    const name = document.getElementById("student-name").value;
    const surname = document.getElementById("student-surname").value;
    const pesel = document.getElementById("student-pesel").value;
    const classId = document.getElementById("class_id").value;

    if (!validateNameOrSurname(name)) {
        alert("Imię może zawierać tylko litery.");
        return;
    }
    if (!validateNameOrSurname(surname)) {
        alert("Nazwisko może zawierać tylko litery.");
        return;
    }
    if (!validatePesel(pesel)) {
        alert("PESEL musi zawierać dokładnie 11 cyfr.");
        return;
    }
    if (!validateClassId(classId)) {
        alert("ID klasy musi zawierać tylko cyfry.");
        return;
    }

    fetch(API_URI + 'add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            surname: surname,
            pesel: pesel,
            class_id: classId
        })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            if (data.message) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Błąd przy dodawaniu ucznia:', error);
        });
}

function deleteStudentFromDb() {
    const id = document.getElementById("student-id").value;

    fetch(API_URI + 'delete', {
        method: 'POST',
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
        alert("Uczeń został usunięty.");
        closeStudentDeleteForm();
        location.reload();
    }).catch(error => {
        console.error('Błąd:', error);
        alert("Nie udało się usunąć ucznia.");
    });
}

function enableEdit(button) {
    const row = button.closest('tr');
    const cells = row.querySelectorAll('td');

    for (let i = 2; i < cells.length - 1; i++) {
        const value = cells[i].innerText;
        cells[i].innerHTML = `<input type="text" value="${value}">`;
    }

    button.innerText = 'Zapisz';
    button.onclick = () => editStudentInDb(row, button);
}

function editStudentInDb(row, button) {
    const cells = row.querySelectorAll('td');
    const id = cells[1].innerText;
    const name = cells[2].querySelector('input').value;
    const surname = cells[3].querySelector('input').value;
    const pesel = cells[4].querySelector('input').value;

    if (!validateNameOrSurname(name)) {
        alert("Imię może zawierać tylko litery.");
        return;
    }
    if (!validateNameOrSurname(surname)) {
        alert("Nazwisko może zawierać tylko litery.");
        return;
    }
    if (!validatePesel(pesel)) {
        alert("PESEL musi zawierać dokładnie 11 cyfr.");
        return;
    }

    fetch(API_URI + 'update', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: id,
            name: name,
            surname: surname,
            pesel: pesel,
        })
    }).then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            if (data.message) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Błąd przy edytowaniu ucznia:', error);
        });
}

function filterByClass() {
    const selectedClassId = document.getElementById('class-filter').value;
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        const classId = row.getAttribute('data-class-id');
        if (selectedClassId === 'all' || classId === selectedClassId) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}