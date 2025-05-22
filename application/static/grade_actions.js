function openGradeAddForm() {
    document.getElementById('grade-add-modal').style.display = 'block';
}

function closeGradeAddForm() {
    document.getElementById('grade-add-modal').style.display = 'none';
    document.getElementById('grade-add-form').reset();
}

function openGradeDeleteForm() {
    document.getElementById('grade-delete-modal').style.display = 'block';
}

function closeGradeDeleteForm() {
    document.getElementById('grade-delete-modal').style.display = 'none';
    document.getElementById('grade-delete-form').reset();
}

function toggleFailures() {
    const showFailures = document.getElementById('show-failure').checked;
    const rows = document.querySelectorAll('#grades-tbody tr');

    rows.forEach(row => {
        const grade = row.cells[2].textContent;
        const isFailure = parseInt(grade) <= 3;

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
        if (selectedClassId === 'all' || classId === selectedClassId) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}