
### Folder Tree ###
```
|── pipelines
        ├── CMakeLists.txt        # Necessary to copy the the files into the folder 
        ├── detector.pipe         # The detector file 
        ├── README.md
        └── species_detector.py   # Plugin created to work with our model
```

### Folders ### 
In order to facilitate the automatic annotation of data, a dedicated folder has been provided, containing the necessary files for creating a pipeline. During the build process, these files need to be placed within this directory using the docker/moorev_prod.Dockerfile. The target location for the pipeline is /home/viameuser/VIAME_DATA/DRIVE_Pipelines/Name of pipeline.

For each pipeline, a folder needs to be created with a name corresponding to the specific pipeline. This folder should contain two types of files: *.pipe and .zip. The .zip file must encapsulate the AI model, as demonstrated by the example file Best_Gibbula_Acquina.zip inside the models folder.
Additionally, there are various file types aside from .zip, including .svm, .cfg, and others, as detailed in this link: [https://github.com/Kitware/dive/blob/main/docs/Dive-Desktop.md#importexport-of-models].

Ensuring the proper functioning of the pipeline requires the incorporation of the appropriate plugin or the utilization of the provided plugins (e.g., netharn, darknet, mmdet). It is imperative that the AI model conforms to the plugin specifications. A custom plugin has been developed based on the netharn_detector.py file, available at [https://github.com/VIAME/VIAME/blob/main/plugins/pytorch/netharn_detector.py]. This custom plugin has been placed within a folder existing in VIAME, along with the necessary CMakeLists.txt.

The current progress indicates that the pipeline is visible and appears capable of execution. However, an unresolved error persists, and efforts are ongoing to identify and rectify the issue.
The error in question is the following : 
```
Caught unhandled std::exception: TypeError: expected str, bytes or os.PathLike object, not NoneType

At:
  /opt/noaa/viame/lib/python3.6/site-packages/ubelt/util_zip.py(341): _open
  /opt/noaa/viame/lib/python3.6/site-packages/ubelt/util_zip.py(254): __init__
  /opt/noaa/viame/lib/python3.6/site-packages/bioharn/detect_predict.py(123): _ensure_upgraded_model
  /opt/noaa/viame/lib/python3.6/site-packages/bioharn/detect_predict.py(298): _ensure_model
  /opt/noaa/viame/lib/python3.6/site-packages/viame/arrows/pytorch/species_detector.py(87): set_configuration

```
### TO DO
- [ ] Resolve the path problem 
- [ ] Ensure to check for any additional errors, and if needed, make modifications to the species_detector or the .pt file to align with their chosen implementation, be it in Darknet or Netharn. Adjustments should be made based on the specific error encountered or the chosen path for modifying the .pt or species_detector.py.
- [ ] Finalize the plugin and the pipeline
