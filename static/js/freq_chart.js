var freq_container = document.getElementById('frecuencia').getContext('2d');
Chart.defaults.global.elements.line.fill = false;

var freq_chart = new Chart(freq_container,{
    type : "line",
    data : {
        labels : [],
        datasets:[
            {
                label:'Tweets por Minuto',
                borderColor: "#3e95cd",
                data:[]
            }
        ]
    },
    options : {
        title: {
            display: true,
            text: 'Frecuencia de Tweets'
        },
        tooltips: {
            mode:'nearest'
        },
        elements: {
            line: {
                tension:0.5,
                borderWidth:1.5,
            },
            point:{
                radius:2
            }
        },
        scales: {
            xAxes:[{
                type:'time',
                time:{
                    unit:'minute',
                    distribution: 'series'
                    }
                }],
            yAxes:[{
                ticks: {
                    beginAtZero: true
                }
            }]
            }
        }
    }
);


const updateFreqChart = (chart, newData) => {

    chart.data.labels = newData.labels;
    chart.data.datasets[0].data = newData.count;
    chart.update();
};


setInterval(
    function () {
        $.getJSON(
            '/counters',
            {},
            function (data) {
               updateFreqChart(freq_chart, data);
            }
        )
    }
    ,20000);


