API_URI = "/students/"

function openStudentAddForm() {
    document.getElementById("student-add-modal").style.display = "block";
}

function closeStudentAddForm() {
    document.getElementById("student-add-modal").style.display = "none";
}

function openStudentDeleteForm() {
    document.getElementById("student-delete-modal").style.display = "block";
}

function closeStudentDeleteForm() {
    document.getElementById("student-delete-modal").style.display = "none";
}

function openStudentEditForm() {
    document.getElementById("student-edit-modal").style.display = "block";
}

function closeStudentEditForm() {
    document.getElementById("student-edit-modal").style.display = "none";
}

function addStudentToDb() {

    const name = document.getElementById("student-name").value;
    const surname = document.getElementById("student-surname").value;
    const pesel = document.getElementById("student-pesel").value;
    const classId = document.getElementById("class_id").value;

    // to jest wysłanie sygnału do end pointu w js, tego się używa żeby sie komunikować z serverem
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

function editStudentInDb() {
    const id = document.getElementById('student-edit-id').value;
    const name = document.getElementById("student-edit-name").value;
    const surname = document.getElementById("student-edit-surname").value;
    const pesel = document.getElementById("student-edit-pesel").value;
    const classId = document.getElementById("class_id-edit").value;
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
            class_id: classId
        })
    }).hen(response => response.json())
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
    console.log(selectedClassId)
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
