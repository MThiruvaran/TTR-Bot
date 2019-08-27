from flask import Flask
from flask import request
from flask import make_response
import requests
import json 
app = Flask(__name__)

@app.route('/webhook', methods=["GET","POST"])

def webhook():
     req = request.get_json(silent=True, force=True)
     intent_name = req["queryResult"]["intent"]["displayName"]
     if(intent_name == 'TrainName'):
         return Train(req)
     return{}

def Train(data):
    action = data['queryResult']['action']
    Train_Number=data['queryResult']['parameters']['number']
    url="http://indianrailapi.com/api/v2/TrainInformation/apikey/44e36297c4381f1537e803126977c4d4/TrainNumber/" + Train_Number + "/"
    ls = requests.get(url).json()
    Trainname=ls['TrainName']
    Source=ls['Code']['Source']
    Destination=ls['Code']['Destination']
    if(action=='Text'):
        return TextResponse(Train_Number,Trainname,Source,Destination)
    return{}
    
def TextResponse(Trnum,Traname,src,dst):
    return{
        "fulfillmentText": "the train number is" + Trnum + " Train name is" +Traname + "Source " +src + "destination" +dst
    }

def stationDetails(data):
    action = data['queryResult']['action']
    url = "http://indianrailapi.com/api/v2/AutoCompleteStation/apikey/44e36297c4381f1537e803126977c4d4/StationCodeOrName/"+ StationCode + "/"
    sd = requests.get(url).json()
    for i in range(0,2):
        Station_name = sd['Station'][i]['NameEn']
        lon = sd['Station'][i]['Longitude']
        lat = sd['Station'][i]['Latitude']

        if(action=='Text'):
                return TextResponse(Station_name,lon,lat)
        return{}
    
def TextResponse(tn,ln,lt):
    return{
        "fulfillmentText": "the train name is" + tn + " is at the latitude " + ln + " and Longitude " + lt
    }

def liveStatus(data):
    action = data['queryResult']['action']
    stationName = data['queryResult']['parameters']['StationName']
    date = data['queryResult']['parameters']['date']
    trn_no = data['TrainNumber']
    lsurl = 'http://indianrailapi.com/api/v2/livetrainstatus/apikey/44e36297c4381f1537e803126977c4d4/trainnumber/' + trn_no + '/date/'+ date +'/'
    ls = requests.get(lsurl).json()
    for x in ls['TrainRoute']:
        if (x['StationName']==stationName):
            sarrival = x['ScheduleArrival']
            aarrival = x['ActualArrival']
    if(action=='Text'):
        return TextResponse(stationName,date,sarrival,aarrival)
    return{}

def TextResponse(sn,d,sa,aa):
    return{
        "fulfillmentText": "the train arrival time for" + sn + "on" +d + "is" +sa + "but actual arrival is" +aa
    }

def PnrStatus(data):
    action = data['queryResult']['action']
    url ="http://indianrailapi.com/api/v2/PNRCheck/apikey/44e36297c4381f1537e803126977c4d4/PNRNumber//Route/1/"


if __name__ == '__main__':
    app.run(port=3000, debug = True)