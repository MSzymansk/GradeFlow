URL = ""

function filterByClass() {
    const selectedClassId = document.getElementById('class-filter').value;
    const rows = document.querySelectorAll('tbody tr');

    rows.forEach(row => {
        const classId = row.getAttribute('data-class-id');

        if (selectedClassId === "brak") {
            row.style.display = 'none';
        } else if (classId === selectedClassId) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}


document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        row.style.display = 'none';
    });
});
function submitAttendance() {
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const classId = document.getElementById('class-filter').value;

    if (classId === "brak") {
        alert("Wybierz klasę przed zapisaniem.");
        return;
    }

    const rows = document.querySelectorAll('tbody tr');
    const attendanceData = [];

    for (let row of rows) {
        if (row.style.display === 'none') continue;

        const studentId = row.getAttribute('data-student-id');
        const radios = row.querySelectorAll(`input[name="status_${studentId}"]`);
        let status = null;
        for (let r of radios) {
            if (r.checked) {
                status = r.value;
                break;
            }
        }

        if (!status) {
            alert(`Nie wybrano statusu dla ucznia ID ${studentId}`);
            return; // przerywa całą funkcję
        }

        attendanceData.push({
            student_id: studentId,
            class_id: classId,
            time: time,
            date: date,
            status: status
        });
    }

    fetch("/attendance/add", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(attendanceData)
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            if (data.success) {
                setTimeout(() => {
                    window.location.href = "/attendance";
                }, 1000);
            }
        })
        .catch(error => {
            console.error("Błąd zapisu obecności:", error);
        });
}
