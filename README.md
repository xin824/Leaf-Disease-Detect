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
  
  - Calling control.py to modify the database of the website.
  - Calling run_process function to predict the image, and update the predict result on the website.
  - To change each model, just modify the path assigned globally on the beginning of the code.
  - This code will record all the cameras that have been connected, and list all of them on the website.
  - Once a new camera connect to the websocket, it will add a new column to the device list of the website.
  - We will save the newest image from the camera as `os.path.join(image_directory, ip_address, f"new.jpg")`
  
  ### main.py
  
  - We use **Flask** to turn our board into a web server, and design API to connect the **SQLAlchemy** and the react app:
      - `save_wifi_ip()`
      use this if the website fail to connect to the database. When we run main.py, this function will automatically be called.
      - `/plants`
      Add this after URL to see all the columns in the database.

  ### models.py
  
  - We design the database here:
    - ip: The ip address of the camera.
    - name: Name of the camera.
    - state: The detect result of the newest image of this camera. The first three character is the healthy ratio from 0 to 100, and the following word is the disease name or "healthy".
    - image_path: "connect" or "disconnect". Save the connection status of the camera.
    - update_time: The save time of the newest image.
    
## flask-server/model/

  ### module.py

  - Main code in processing images received by esp32 camera.
  - Import each model class and each model processing code.
  - Using NeuronRuntimeHelper API to maximize the performance.

  ### *_process.py

  - Using each model to predict the image and return output to caller.

  ### transforma_*.py
  
  - Define model class and some self function that can be used when processing data.

## plant/
  - In the main page of the website, all the cameras that have been connected will be listed on the website. 
  - On the left, the wifi icon show the connection status of the camera.
  - Press the button on the right for more details.
  ![main_page](https://github.com/xin824/Leaf-Disease-Detect-Website/blob/master/readme/main_page.png)
  - The detail page show the disease name, healthy rate, last updated time of the image, and the newest image from the camera or model.
  - We can modify the name by press the pencil icon.
  ![detail_page](https://github.com/xin824/Leaf-Disease-Detect-Website/blob/master/readme/detail_page.png)
  - Pressing the solution button, the website will help us to manage our plant.
![solution](https://github.com/xin824/Leaf-Disease-Detect-Website/blob/master/readme/solution.png)
  - The website is built with **React**, after modify a script, run `$ npm run build` and the flask server will automatically update the website.
  - By reading the wifi_ip.txt, the website  connect to database. If something went wrong, please check whether the context of this file is same as the URL generated from Flask.
  
  ### src/App.tsx
  
  - We control the database fetch rate here.
      ```
      const interval = setInterval(() => {
          onUpdate();
        }, 350); //350ms
      ```
  ### src/components/PlantCard.tsx
  
  - We control the image refresh rate here, 
    ```
    useInterval(() => {
    　　const timestamp = new Date().getTime()
  	　　setImgURL(`./image/${plant?.ip}/annotation.jpg?t=${timestamp}`)  
	}, 300);
    ```
    If the interval is smaller than model detection speed, the refresh rate will depend on the model speed, or it will update every 300ms consistently.
    
## Demo Video
