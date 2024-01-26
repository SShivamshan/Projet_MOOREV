FROM shivamshan/moorev_viame

# To copy the images in a folder to the docker container : 
COPY ../dataset/test /home/viameuser/images

# To copy the pipelines needed for that automatic annotation of data in VIAME
USER viameuser
RUN mkdir -p /home/viameuser/VIAME_DATA/DIVE_Jobs \
             /home/viameuser/VIAME_DATA/DIVE_Projects \
             /home/viameuser/VIAME_DATA/DIVE_Pipelines \
             /home/viameuser/VIAME_DATA/DIVE_Pipelines/Acuqinia

COPY ../pipelines/detector.pipe /home/viameuser/VIAME_DATA/DIVE_Pipelines/Acuqinia/detector.pipe
# COPY ../models/best_Gibbula-Actinia.pt /opt/noaa/viame/configs/pipelines/models/best_Gibbula-Actinia.pt
COPY ../pipelines/species_detector.py /opt/noaa/viame/lib/python3.6/site-packages/viame/arrows/pytorch/species_detector.py
COPY ../models/best_Gibbula-Actinia.zip /home/viameuser/VIAME_DATA/DIVE_Pipelines/Acuqinia/best_Gibbula-Actinia.zip

