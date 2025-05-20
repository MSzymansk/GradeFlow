API_URI = "/students/"

function openStudentForm() {
    document.getElementById("student-modal").style.display = "block";
}

function closeStudentForm() {
    document.getElementById("student-modal").style.display = "none";
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