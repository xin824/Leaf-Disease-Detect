# VIA Project-Leaf Disease Detect

## How to run?
  
  *Better setup a virtual environment in order to run safely on your computer.*
  
  - Open two terminals to run main.py and receive_stream_final.py. 
  -- main.py
      - Setup virtual environment at **/flask-server**:
      ```
      $ source venv/bin/activate
      $ python3 main.py
      ```
      
      - Then we can get the URL of our website to check our result.
  
      -- receive_stream_final.py
      - Also setup virtual environment to run this process.
      ```
      $ source venv/bin/activate
      $ python3 receive_stream_final.py
      ```
      - After executing the code above, turn on your camera to connect to the board.


## flask-server/

  ### receive_stream_final.py
  
  - Calling run_process function to predict the image.
  - To change each model, just modify the path assigned globally on the beginning of the code.

## flask-server/model/

  ### module.py

  - Main code in processing images received by esp32 camera.
  - Import each model class and each model processing code.
  - Using NeuronRuntimeHelper API to maximize the performance.

  ### *_process.py

  - Using each model to predict the image and return output to caller.

  ### transforma_*.py
  
  - Define model class and some self function that can be used when processing data.

