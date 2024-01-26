
### Folder Tree ###
|── docker                
    │   ├── chrome.json                            
    │   ├── moorev_prod.Dockerfile  
    |   ├── moorev_dev.Dockerfile  
    |   └── README.md 
    
### Folders ### 
This folder contains the dockerfile for creating the VIAME installation with all its dependencies and another dockerfile for using this docker image as it's based which will be used for the production.
**It's necessary to install the NVIDIA-Container Toolkit in order for the pipelines to work properly : https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html**

### Dev dockerfile 
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

### Prod dockerfile
The production dockerfile uses the docker image that we created using the dev dockerfile which is also available on the docker hub.  
For the moorev_prod.Dockerfile we need the same flags from before but also the following flag as well : 
- -v exports:/home/viameuser/exports is a docker
   volume so that we can retrieve the downloaded file
  
To build the dockerfile for prod, you need to first pull the docker image that we created : `sudo docker pull shivamshan/moorev_viame` from the terminal or directly download it : https://hub.docker.com/r/shivamshan/moorev_viame
We first pulled the docker image directly since it's a large image(22.2Gb) and since this will fasten the process. 
Then run this command to build it's necessary to be in the Projet_moorev folder and run this command : `sudo docker build -t docker_image_name -f docker/moorev_prod.Dockerfile .` since the moorev_prod.Dockerfile uses the image that we pulled before the building of this dockerfile is fast(0.5s at most). 

The final command would looks like this for the prod dockerfile in order to run it : `sudo docker run -p 9876:9876 --gpus all -it --name container name -e DISPLAY=:1 --security-opt seccomp=docker/chrome.json -e ELECTRON_ENABLE_LOGGING=true -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/.Xauthority:/root/.Xauthority --mount type=bind,source="$(pwd)"/export,target=/home/viameuser/export --mount type=bind,source="$(pwd)"/dataset/images,target=/home/viameuser/image docker container name`

This command will launch VIAME Desktop on the web accessible through the following URL : http://localhost:9876/

To facilitate the transfer of images and retrieve annotated data with VIAME, we utilize the --mount option to bind mount host directories into the Docker container.
### Mounting the Dataset of Images

To provide the Docker container access to a dataset containing images, we use the following mount command:
- `--mount type=bind,source="$(pwd)"/dataset/images,target=/home/viameuser/images` 
 - **source**: This represents the path to the host directory containing the images. The $(pwd) command dynamically fetches the current working directory.
 - **target**: Specifies the path inside the Docker container where the images will be available. In this case, the target directory is /home/viameuser/images.

### Mounting a Directory for Exporting Annotated Data
To ensure the Docker container can export annotated data directly to the host machine, we employ the following mount command:

- `--mount type=bind,source="$(pwd)"/export,target=/home/viameuser/export`
 - **source**: Indicates the path to the host directory where annotated data will be saved. The $(pwd) command dynamically fetches the current working directory.
 - **target**: Specifies the path inside the Docker container where the export directory is accessible. In this case, the target directory is /home/viameuser/export.


