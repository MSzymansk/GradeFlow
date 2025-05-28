let avgClassChart, gradesByClassChart;
function createAvgClassChart(data) {
    const ctx = document.getElementById('avgClassChart').getContext('2d');

    const classAvgs = {};
    data.forEach(student => {
        if (!classAvgs[student.class_name]) {
            classAvgs[student.class_name] = [];
        }
        classAvgs[student.class_name].push(parseFloat(student.avg));
    });

    const classNames = Object.keys(classAvgs);
    const averages = classNames.map(className => {
        const arr = classAvgs[className];
        return (arr.reduce((a,b) => a + b, 0) / arr.length).toFixed(2);
    });

    const chartData = {
        labels: classNames,
        datasets: [{
            label: 'Średnia ocen',
            data: averages,
            backgroundColor: '#4CAF50'
        }]
    };

    avgClassChart = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {min: 1, max: 6}
            }
        }
    });
}
function createGradesByClassChart(data) {
    const ctx = document.getElementById('gradesByClassChart').getContext('2d');

    const classGradesCount = {};
    data.forEach(student => {
        if (!classGradesCount[student.class_name]) {
            classGradesCount[student.class_name] = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0};
        }
        student.grades_list.forEach(grade => {
            if (classGradesCount[student.class_name][grade] !== undefined) {
                classGradesCount[student.class_name][grade]++;
            }
        });
    });

    const classNames = Object.keys(classGradesCount);
    const grades = ['1','2','3','4','5','6'];

    const colors = ['#d32f2f', '#f57c00', '#fbc02d', '#388e3c', '#1976d2', '#7b1fa2'];
    const datasets = grades.map((grade, idx) => ({
        label: `Ocena ${grade}`,
        data: classNames.map(className => classGradesCount[className][grade]),
        backgroundColor: colors[idx]
    }));

    const chartData = {
        labels: classNames,
        datasets: datasets
    };

    gradesByClassChart = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true }
            },
            plugins: {
                legend: { position: 'top' }
            }
        }
    });
}

async function fetchRealData() {
    const gradesData = await fetch('/grades/get_grades_for_chart').then(r => r.json());
    const studentsData = await fetch('/students/get_all_students_for_chart').then(r => r.json());

    createAvgClassChart(studentsData);
    createGradesByClassChart(gradesData);
}

document.addEventListener('DOMContentLoaded', () => {
    fetchRealData();
});
