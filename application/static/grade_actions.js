API_URI = "/grades/"

function openGradeAddForm(button) {
    const row = button.closest('tr');
    document.getElementById('hidden-student-id').value = row.dataset.studentId;

    document.getElementById('grade-add-modal').style.display = 'block';
}

function closeGradeAddForm() {
    document.getElementById('grade-add-modal').style.display = 'none';
    document.getElementById('grade-add-form').reset();
}

function addGradeToDb() {
    const value = document.getElementById('grade-value').value;
    const type = document.getElementById('grade-type').value;
    const studentId = document.getElementById('hidden-student-id').value;
    console.log("test")
    const validValues = [1, 2, 3, 4, 5, 6]
    if (!validValues.includes(parseInt(value))) {
        alert("Wartość oceny jest niepoprawne")
        return
    }

    if (!type){
        alert("Wybierz typ oceny")
        return
    }

    fetch(API_URI + 'add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            value: value,
            type: type,
            student_id: studentId
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
            console.error('Błąd przy dodawaniu oceny:', error);
        });

}


function toggleFailures() {
    const showFailures = document.getElementById('show-failure').checked;
    const rows = document.querySelectorAll('#grades-tbody tr');

    rows.forEach(row => {
        const avg = row.cells[6].textContent;
        const isFailure = parseFloat(avg) < 3;

        if (showFailures && isFailure) {
            row.classList.add('failure-row');
        } else {
            row.classList.remove('failure-row');
        }
    });
}

function filterByClass() {
    const selectedClassId = document.getElementById('class-filter').value;
    const rows = document.querySelectorAll('tbody tr');

    rows.forEach(row => {
        const classId = row.getAttribute('data-class-id');
        const showAll = selectedClassId === "all";
        if (showAll || String(classId) === String(selectedClassId)){
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}