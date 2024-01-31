FROM shivamshan/moorev_viame

USER root

# To copy the trained models into VIAME
COPY --chown=viameuser:viameuser ../pipelines/detector.pipe /home/viameuser/VIAME_DATA/DIVE_Pipelines/Acuqinia/detector.pipe
COPY --chown=viameuser:viameuser ../models/best_Gibbula_Actinia.zip /home/viameuser/VIAME_DATA/DIVE_Pipelines/Acuqinia/best_Gibbula_Actinia.zip
RUN chmod 644 /home/viameuser/VIAME_DATA/DIVE_Pipelines/Acuqinia/best_Gibbula_Actinia.zip

# To copy the pipelines needed for that automatic annotation of data in VIAME
USER viameuser

RUN mkdir -p /home/viameuser/VIAME_DATA/DIVE_Jobs \
             /home/viameuser/VIAME_DATA/DIVE_Projects \
             /home/viameuser/VIAME_DATA/DIVE_Pipelines \
             /home/viameuser/VIAME_DATA/DIVE_Pipelines/Acuqinia 
             # The Acuqinia folder is the name of pipeline that will appear in the the trained section of Pipeline inside the interface

# Plugin placed inside an already existing folder of VIAME
COPY --chown=viameuser:viameuser ../pipelines/species_detector.py /opt/noaa/viame/lib/python3.6/site-packages/viame/arrows/pytorch/species_detector.py
COPY --chown=viameuser:viameuser ../pipelines/CMakeLists.txt /opt/noaa/viame/lib/python3.6/site-packages/viame/arrows/pytorch/CMakeLists.txt

