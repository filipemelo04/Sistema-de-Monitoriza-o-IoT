from fastapi import FastAPI
from influxdb import InfluxDBClient
from datetime import datetime
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

plant_list = ["external", "tomatos", "coentro", "salsa"]
measurement_list = ["temperature", "humidity"]

#	 METODO PARA TESTE
@app.get("/")
def home():
	return {"Data": "Teste"}
	

# 	METODO QUE RETORNA OS VALORES ATUAIS	
@app.get("/get_current_value/{plant_type}/{measur_type}")
def get_current_value(plant_type: str, measur_type: str):
	client = InfluxDBClient(host='localhost', port='8086')
	client.switch_database('FilipeFarm')
	
	plant_type = plant_type.lower()
	measur_type = measur_type.lower()

	if (plant_type in plant_list)  and (measur_type in measurement_list):		
		result = client.query("".join(['''select last(''', '''"''', measur_type, '''"''', ''') from "internal_farm" where "plant"=''',"'", plant_type, "'",''';''']))		
		dataPoints = list(result.get_points())			
		return {"Data": dataPoints[0]['last']}
		
	else: return {"Data": "Query not valid"}	


#	METODO QUE RETORNA UM ARRAY COM A MÉDIA DIáRIA DO ULTIMO MêS
@app.get("/get_average_month/{plant_type}/{measur_type}")   
def get_average_month(plant_type: str, measur_type: str):        
	client = InfluxDBClient(host='localhost', port='8086')
	client.switch_database('FilipeFarm')

	plant_type = plant_type.lower()
	measur_type = measur_type.lower()
	
	if (plant_type in plant_list)  and (measur_type in measurement_list):		
		result = client.query("".join(['''select ''', '''"''', measur_type, '''"''', ''' from "Average_Data" where "plant"=''',"'", plant_type, "'",''' AND time > now() - 30d;''']))		
		dataPoints = list(result.get_points())			
		for i in range(len(dataPoints)):
			dataPoints[i]['time'] = dataPoints[i]['time'][:dataPoints[i]['time'].find(".")]
			dataPoints[i]['time'] = dataPoints[i]['time'].replace("T", " ")	
		return dataPoints
				
	else: return {"Data": "Query not valid"}
	

# 	METODO QUE RETORNA 
@app.get("/get_day_values/{plant_type}/{measur_type}")
def get_day_values(plant_type: str, measur_type: str):
	client = InfluxDBClient(host='localhost', port='8086')
	client.switch_database('FilipeFarm')	
	
	plant_type = plant_type.lower()
	measur_type = measur_type.lower()	
	
	if (plant_type in plant_list)  and (measur_type in measurement_list):		
		result = client.query("".join(['''select ''', '''"''', measur_type, '''"''', ''' from "internal_farm" where "plant"=''',"'", plant_type, "'",''' AND time > now() - 1d;''']))		
		dataPoints = list(result.get_points())
			
		for i in range(len(dataPoints)):
			dataPoints[i]['time'] = dataPoints[i]['time'][:dataPoints[i]['time'].find(".")]
			dataPoints[i]['time'] = dataPoints[i]['time'].replace("T", " ")
		return dataPoints
			
	else: return {"Data": "Query not valid"}
	
	
	
	
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
	
	
