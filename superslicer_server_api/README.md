# SuperSlicer Server API

---

The API server for accessing SuperSlicer from the web. It allows slice a 3D model with specific settings passed as a JSON, 
download the G-code file result. This is a basic server that runs from the command line (not as a service). One can create
a service to use the **_run.sh_** script file.



## Installation

1. Download the folder or clone the repository
   1. ``` 
       git clone https://DOMAIN/superslicer_sever.git 
      ```
2. Run the installation script located in the **scripts** directory
   1. ```
       ./install.sh
      ```

This will create the Python3 virtual environment and install all the [requirements](/requirements.txt).
**It requires then a Python3 installation on the host machine**.

## Usage
For basic usage, in the **scripts** directory, launch the server as followed :
```{r}
    ./run.sh
```
The server will listen on the port 5000 and all interfaces. Open the port 5000 through the firewall
to allow connection. From an API tools, access the server with **http://{IP}:5000/** (replace {IP} by the IP of the host machine).

## Endpoints

The API server exposes the following endpoints :

- / : [**METHOD : GET**] => endpoint that returns some information on the server
  ```
        {
            'name': 'SuperSlicer Server',
            'description': 'API Web Server for SuperSlicer',
            'version': '1.0.0',
            'author': 'Normil Jose',
            'website': '',
            'repos': 'github'
        }
  ```
- /slice : [**METHOD : POST**] => endpoint for uploading the 3D model file (STL,OBJ,AMF) and the settings as JSON, then send them to the **_SuperSlicer_**.
    => returns a response like followed :
  ```
        {
            'message': 'File uploaded successfully. Check the result in the G-code viewer.',
            'file': {filename.ext}
        }
  ```
- /slice/{filename.ext} : [**METHOD : GET**] : endpoint for the realtime tracking of the slicing operation (**NOT WORKING**). It checks if the G-code result existed on the server for the filename specified
  and returns a response like followed :
  ```
        {
            'message': 'The slicing of {filename.ext} has finished'
        }
  ```
- /files/stl/(.*) : [**METHOD : GET**] : endpoint for downloading an STL file uploaded for slicing or to know the number of files in the _stls_ folder.
- /files/obj/(.*) : [**METHOD : GET**] : endpoint for downloading an OBJ file uploaded for slicing or to know the number of files in the _objs_ folder.
- /files/amf/(.*) : [**METHOD : GET**] : endpoint for downloading an AMF file uploaded for slicing or to know the number of files in the _amfs_ folder.
- /files/gcode/(.*) : [**METHOD : GET**] : endpoint for downloading a G-code file resulting from the slicing operation or to know the number of files in the _gcodes_ folder.