
### Folder Tree ###
```
|── docker                
    │   ├── chrome.json                            
    │   ├── moorev_prod.Dockerfile  
    |   ├── moorev_dev.Dockerfile  
    |   └── README.md 
```
### Folders ### 
This directory comprises two Dockerfiles: one for building the VIAME installation along with all its dependencies, and another for utilizing the resultant Docker image as a base. The latter will be employed for production purposes.

**It is imperative to install the NVIDIA-Container Toolkit to ensure the proper functioning of the pipelines. For installation instructions, please refer to: [https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html]**


### Dev dockerfile 
The moorev_dev.Dockerfile enables the creation of a Docker image encompassing the entire VIAME Desktop installation. To acquire the VIAME Desktop installation, please download it from the following webpage: [https://github.com/VIAME/VIAME#installations].

To execute this Dockerfile, ensure that the following flags are passed during the docker run command: 
`sudo docker run `  
- -p for the port
- --gpus all : to give access to the GPU of the host machine
- -e for the environment variables : in this case the display
- --security-opt seccomp=docker/chrome.json for the system call filtering where the docker/chrome.json file is necessary to run the chromium for electron
- -v /tmp/.X11-unix:/tmp/.X11-unix for X windows system in order to run the graphical application inside the docker and display it 
- -v $HOME/.Xauthority:/root/.Xauthority needed for the authentification of X window system for the GUI to run properly

n the final command, such as for the developpement Dockerfile, replace <desired_port>, <container_name>, and <docker_image_name> with the appropriate values. For example: : `sudo docker run -p 9876:9876 -it --gpus all --name page_web -e DISPLAY=:1 --security-opt seccomp=docker/chrome.json -e ELECTRON_ENABLE_LOGGING=true -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/.Xauthority:/root/.Xauthority docker_image name`

### Prod dockerfile
The production Dockerfile (moorev_prod.Dockerfile) utilizes the Docker image created using the development Dockerfile, which is also accessible on the Docker Hub.
To run the moorev_prod.Dockerfile, you will require the same flags as mentioned earlier, and additionally, include the following flag:
- -v exports:/home/viameuser/exports is a docker
   volume so that we can retrieve the downloaded file
  
To build the production Dockerfile, start by pulling the previously created Docker image using the following command in the terminal: `sudo docker pull shivamshan/moorev_viame` Alternatively, you can download the image directly from the Docker Hub: [https://hub.docker.com/r/shivamshan/moorev_viame].
Ensure that the necessary Docker image is available before proceeding with the construction of the production Dockerfile. 

To expedite the process, it is recommended to pull the Docker image directly, especially considering its substantial size (22.2 GB). Once the image has been successfully pulled, navigate to the Projet_moorev folder and execute the following command to initiate the build process: `sudo docker build -t docker_image_name -f docker/moorev_prod.Dockerfile .` since the moorev_prod.Dockerfile uses the image that we pulled before the building of this dockerfile is fast(0.5s at most). 

The final command would looks like this for the prod dockerfile in order to run it : `sudo docker run -p 9876:9876 --gpus all -it --name container name -e DISPLAY=:1 --security-opt seccomp=docker/chrome.json -e ELECTRON_ENABLE_LOGGING=true -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/.Xauthority:/root/.Xauthority --mount type=bind,source="$(pwd)"/export,target=/home/viameuser/export --mount type=bind,source="$(pwd)"/dataset/images,target=/home/viameuser/image docker container name`

This command initiates VIAME Desktop for web access, accessible through the URL: [http://localhost:9876/].

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


