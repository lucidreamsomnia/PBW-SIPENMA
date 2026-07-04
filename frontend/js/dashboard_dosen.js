// Pie Chart Kelulusan

new Chart(
    document.getElementById("kelulusanChart"),
    {
        type: "pie",

        data: {
            labels: [
                "Lulus",
                "Tidak Lulus"
            ],

            datasets: [{
                data: [
                    280,
                    60
                ]
            }]
        }
    }
);


// Bar Chart Mata Kuliah

new Chart(
    document.getElementById("matkulChart"),
    {
        type: "bar",

        data: {
            labels: [
                "Basis Data",
                "PBW",
                "Jaringan",
                "AI",
                "PPDM"
            ],

            datasets: [{
                label: "Rata-rata Nilai",

                data: [
                    82,
                    85,
                    78,
                    80,
                    84
                ]
            }]
        }
    }
);