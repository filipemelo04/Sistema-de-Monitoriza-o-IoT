
const apiOrigin = 'http://192.168.1.130:8080';

// FAZ GET A TEMPERATURA ATUAL
async function current_temperature(){

	const response = await fetch(apiOrigin + '/get_current_value/external/temperature');
 	const data = await response.json();
    document.getElementById("demo").innerHTML = data['Data'];
}
current_temperature();

// FAZ GET A HUMIDADE ATUAL
async function current_humidity(){

	const response = await fetch(apiOrigin + '/get_current_value/external/humidity');
 	const data = await response.json();
    document.getElementById("demo1").innerHTML = data['Data'];
}
current_humidity();


// FAZ GRAFICO COM TEMPERATURA/HUMIDADE AMBIENTE
async function temperature_graphic_lastday(){

	const response_temp = await fetch(apiOrigin + '/get_day_values/external/temperature');
 	const data_temp = await response_temp.json();

    const response_hum = await fetch(apiOrigin + '/get_day_values/external/humidity');
 	const data_hum = await response_hum.json();

	x_axis_temp = []
	y_axis_temp = []
	for (var i = 0; i < data_temp.length; i++) {
		x_axis_temp.push(data_temp[i]['time'])
		y_axis_temp.push(data_temp[i]['temperature'])
	}

    y_axis_hum = []
	for (var i = 0; i < data_hum.length; i++) {
		y_axis_hum.push(data_hum[i]['humidity'])
	}

    if (y_axis_temp.length != y_axis_hum.length) {
        var dif = y_axis_temp.length - y_axis_hum.length
        if (dif < 0) {
            for (var i=0; i<-dif; i++){
                y_axis_hum.pop()
            }
        }
        if (dif > 0) {
            for (var i=0; i<dif; i++){
                y_axis_temp.pop()
            }
        }
    }

	// Creating line chart
	let ctx1 = document.getElementById('grafico_temperatura_ambiente').getContext('2d');
	let myLineChart1 = new Chart(ctx1, {
		type: 'line',
		data: {
            labels: x_axis_temp,
            datasets: [
              {
                label: 'Temperatura (ºC)',
                data: y_axis_temp,
                borderColor: 'red',
                backgroundColor: 'blue',
                yAxisID: 'y',
              },
              {
                label: 'Humidade (%)',
                data: y_axis_hum,
                borderColor: 'green',
                backgroundColor: 'grey',
                yAxisID: 'y1',
              }
            ]
        },
		options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: true,
            },
            stacked: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Gráfico Linha: Temperatura/Humidade Ambiente'
                }
            },
            scales: {
                y: {
					title: {
						display: true,
						text: 'ºC',
						font: {
							padding: 4,
							size: 20,
							weight: 'bold',
							family: 'Arial'
						},
						color: 'red'
					},
                    type: 'linear',
                    display: true,
                    position: 'left',
                },
                y1: {
					title: {
						display: true,
						text: '%',
						font: {
							padding: 4,
							size: 20,
							weight: 'bold',
							family: 'Arial'
						},
						color: 'green'
					},
                    type: 'linear',
                    display: true,
                    position: 'right',
            
                    // grid line settings
                    grid: {
                    drawOnChartArea: false, // only want the grid lines for one axis to show up
                    },
                },
            }
        },
	});

}
temperature_graphic_lastday();


// Atualiza a data

function loadDate() {
    let date = new Date(),
        day = date.getDate(),
        month = date.getMonth() + 1,
        year = date.getFullYear();

    if (month < 10) month = "0" + month;
    if (day < 10) day = "0" + day;

    const todayDate = `${year}-${month}-${day}`;

    document.getElementById("start_date").defaultValue = todayDate;
};
loadDate();

/*function load_start_final_date() {
	let start_date = document.getElementById("start_date").value;
	let final_date = document.getElementById("final_date").value; 
}*/

// FAZ GRAFICO DOS VASOS
async function temperature_graphic_lastday_byPlant(){

	let plant = document.querySelector('#planta');
	let optionValue = plant.options[plant.selectedIndex].value;
	//console.log(optionValue);

	/*let start_date = document.querySelector('#start_date');
	console.log(start_date);*/

	let path = '/get_day_values/' + optionValue + '/temperature';
	//console.log(path);

	const response = await fetch(apiOrigin + path);
 	const data = await response.json();
	//console.log(data);
    //alert(data['Data'])
	// data for showing the line chart
	x_axis = []
	y_axis = []
	for (var i = 0; i < data.length; i++) {
		x_axis.push(data[i]['time'])
		y_axis.push(data[i]['temperature'])
	}
	
	// Creating line chart
	const config2 = {
		type: 'line',
		data: {
			labels: x_axis,
			datasets: [
				{
					label: 'Linha Temperatura',
					data: y_axis,
					borderColor: 'blue',
					borderWidth: 1, //2
					fill: false,
				}
			]
		},
		options: {
			responsive: true,
			scales: {
				x: {
					title: {
						display: true,
						text: 'Data Tempo',
						font: {
							padding: 4,
							size: 20,
							weight: 'bold',
							family: 'Arial'
						},
						color: 'darkblue'
					}
				},
				y: {
					title: {
						display: true,
						text: 'Temperatura °C',
						font: {
							size: 20,
							weight: 'bold',
							family: 'Arial'
						},
						color: 'darkblue'
					},
					beginAtZero: false,
					scaleLabel: {
						display: true,
						labelString: 'Values',
					}
				}
			}
		}
	}

	let ctx2 = document.getElementById('myChart').getContext('2d');
	
	let myLineChart2 = new Chart(ctx2, config2);

	const planta = document.getElementById('planta');
	planta.addEventListener('change', plantTracker);

	function plantTracker(){
		console.log(planta.value);
		myLineChart2.data.datasets[0].data = [5,4,8,1,6,25,14,25,14,14,13,14]
		myLineChart2.update();
	}

}
temperature_graphic_lastday_byPlant()


