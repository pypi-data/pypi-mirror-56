# Python Data Plugin

## Introduction
A python plugin to load data from any connected data platform e.g. sponsored-data, marketing console e.t.c.
to a connected API.

### Technologies
Python==3.7.2  
requests==2.22.0

### Method
Method: send_data(data_container)  

The data_container should be a dictionary if you want to send a single data e.g  
send_data({'data_source': source, 'data_type': type, 'data': data})  

The data_container should be a list of dictionaries if multiple data are to be sent

### Valid data sources
- Marketing console 
- Sponsored data
- Trivia  
- survey-interactive-messaging
### Valid data types
- Demography
- Transactional
- Billing  
- conversion
- survey


### How to Launch
##### Pip install the package  
pip install terra_python_plugin  
### Using the module
from terra_python_plugin import terra_python_plugin  
plugin = terra_python_plugin.PythonPlugin()    
plugin.send_data(  
        [  
            {"data_source": 'test', "data_type": 'topic', "data": 23237873823},  
            {"data_source": 'test', "data_type": 'topic', "data": "testing 1223"},  
            {"data_source": 'test', "data_type": 'topic', "data": "tested 001"}  
        ]   
    )

#### Who can i talk to
Adeyeye Timothy  
tadeyeye@terragonltd.com