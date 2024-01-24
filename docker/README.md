
### Folder Tree ###
|── docker                
    │   ├── chrome.json                            
    │   ├── moorev_prod.Dockerfile  
    |   ├── moorev_dev.Dockerfile  
    |   └── README.md 
    
### Folders ### 
This folder contains the dockerfile for creating the VIAME installation with all its dependencies and another dockerfile for using this docker image as it's based which will be used for the production.
**It's necessary to install the NVIDIA-Container Toolkit in order for the pipelines to work properly : https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html**
#### Dev dockerfile 
The moorev_dev.Dockerfile allows to create a docker image with all VIAME Desktop installation. The VIAME Desktop installation needs to be downloaded througth this web page : https://github.com/VIAME/VIAME#installations 
In order to run this dockerfile, you need to pass the following flags during the docker run : 
`sudo docker run `  
- -p for the port
- --gpus all : to give access to the GPU of the host machine
- -e for the environment variables : in this case the display
- --security-opt seccomp=docker/chrome.json for the system call filtering where the docker/chrome.json file is necessary to run the chromium for electron
- -v /tmp/.X11-unix:/tmp/.X11-unix for X windows system in order to run the graphical application inside the docker and display it 
- -v $HOME/.Xauthority:/root/.Xauthority needed for the authentification of X window system for the GUI to run properly

The final command would looks like this for the prod dockerfile : `sudo docker run -p 9876:9876 -it --gpus all --name page_web -e DISPLAY=:1 --security-opt seccomp=docker/chrome.json -e ELECTRON_ENABLE_LOGGING=true -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/.Xauthority:/root/.Xauthority docker_image name`

#### Prod dockerfile
The production dockerfile uses the docker image that we created using the dev dockerfile which is also available on the docker hub.  
For the moorev_prod.Dockerfile we need the same flags from before but also the following flag as well : 
- -v exports:/home/viameuser/exports is a docker
   volume so that we can retrieve the downloaded file
To build the dockerfile for prod, you need to first pull the docker image that we created : `sudo docker pull shivamshan/moorev_viame` from the terminal or directly download it : https://hub.docker.com/r/shivamshan/moorev_viame
We first pulled the docker image directly since it's a large image(22.2Gb) and since this will fasten the process. 
Then run this command to build it's necessary to be in the Projet_moorev folder and run this command : `sudo docker build -t docker_image_name -f docker/moorev_prod.Dockerfile .` since the moorev_prod.Dockerfile uses the image that we pulled before the building of this dockerfile is fast(0.5s at most). 

The final command would looks like this for the prod dockerfile in order to run it : `sudo docker run -p 9876:9876 -it --gpus all --name container_name -e DISPLAY=:1 --security-opt seccomp=docker/chrome.json -e ELECTRON_ENABLE_LOGGING=true -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/.Xauthority:/root/.Xauthority -v -v exports:/home/viameuser/exports docker_image name`

This command will launch VIAME Desktop on the web accessible through the following URL : http://localhost:9876/

There is a exports folder inside the docker container which is where the user should download their data to in order for us to retrieve them. 
Usually on the system they are mounted at this location for different OS : 
- Linux : /var/lib/docker/volumes
- Windows : C:\ProgramData\docker\volumes

In which in our case the /var/lib/docker/volumes/exports/_data contains the user's downloaded data

As for to how to bring or put new images inside the docker image you just need to copy them from the host machine to the the docker image : 
- COPY ../dataset/test /home/viameuser/images
This also could be done for the pipelines that we have implemented, they only need to copied to the correct folder inside the docker image. 


