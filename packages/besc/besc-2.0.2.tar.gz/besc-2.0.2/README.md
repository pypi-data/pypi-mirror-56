# besc-ESS-nodejs-client



All working examples is inside the example folder

**0.1dev**

**Added checksum feature**

For those who are not using this client, need to add in few header for it. Data send to ESS API need to be in json format as below and in orders :
```js
{
    "Project" : "",
    "DateTime" : "2019-05-23T06:00:00",
    "Devices": [ 
    { 
 	"DeviceId": "AC11", 
	"EnergyUsage": 130.0 
    },
    {
	"DeviceId": "AC22", 
	"EnergyUsage": 180.0 
    }
    ], 
    "TotalEnergyUsage": 310.0, 
    "AverageRT": 188.0, 
    "Geolocation": "Selangor"
}
```

## Header

Content-Type
- application/json

**apikey**
- the apikey string that get from BESC

**checksum**
- need to be added in header
- sha1 string of the whole json data
- JSON.stringify(object)

As example for checksum,
```js
var object = {
    Project : "",
    DateTime : "2019-05-23T06:00:00",
    Devices: [ 
    { 
	DeviceId: "AC11", 
	EnergyUsage: 130.0 
    },
    {
	DeviceId: "AC22", 
	EnergyUsage: 180.0 
    }
    ], 
    TotalEnergyUsage: 310.0, 
    AverageRT: 188.0, 
    Geolocation: "Selangor"
};

var checksum = sha1( JSON.stringify(object) );

```
Then send the object as JSON to the ESS API.


