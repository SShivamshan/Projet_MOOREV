## Project MOOREV: Annotation and Analysis of Underwater Species Images and Videos
![Alt Text](results/logo.jpg)

## 🎯 *Project Objective*
1. **Image and Video Annotation:** Annotation methods for images using the [VIAME](https://github.com/VIAME/VIAME?tab=readme-ov-file) tool, providing image and video annotation for various users such as researchers, students, teachers, educational facilitators, and volunteers. The web platform is accessible at [viame.kitware.com](https://viame.kitware.com/#/).

2. **Species Recognition through Machine Learning:** Recognition of target species using AI techniques by training models for recognition, segmentation, and tracking with [Ultralytics](https://www.ultralytics.com/fr/) [YOLOv8](https://github.com/ultralytics/ultralytics).

3. **Quantification of Morphological and Behavioral Characteristics:** Investigation of the quantification of individual morphological characteristics (size, shape, and color) and behavior using tools from the [OpenCV](https://opencv.org/) library in Python.

4. **Access to Tools:** All tools are accessible on the [Galaxy-Ecology Europe](https://usegalaxy.eu/) portal to make these image annotation and analysis methods available to online users.

## 🤝 *Authors*
- Islem KOBBI
- Lynda FEDDAK
- Shivamshan SIVANESAN
- Sofiane OUALI

## 📚 *Project Structure*

- **/[`Galaxy Dev`](https://github.com/SShivamshan/Projet_MOOREV/tree/main/Galaxy%20Dev) :** This directory contains XML scripts for launching tools for the annotation and analysis of underwater species images and videos from the Galaxy platform.

- **/[`docker`](https://github.com/SShivamshan/Projet_MOOREV/tree/main/docker) :** This directory includes the file [`moorev_dev.Dockerfile`](https://github.com/SShivamshan/Projet_MOOREV/blob/main/docker/moorev_dev.Dockerfile) for creating the VIAME installation with all its dependencies, as well as another [`moorev_prod.Dockerfile`](https://github.com/SShivamshan/Projet_MOOREV/blob/main/docker/moorev_prod.Dockerfile) for using this Docker image as a base, which will be used for production.
- **/[`docs`](https://github.com/SShivamshan/Projet_MOOREV/tree/main/docs) :** The directory contains the project documentation
- **/[`models`](https://github.com/SShivamshan/Projet_MOOREV/tree/main/models) :** The directory contains the trained YOLOv8 models (.pt files)
- **/[`pipelines`](https://github.com/SShivamshan/Projet_MOOREV/tree/main/pipelines) :** This directory contains the necessary files for creating a pipeline
 .pt files for models trained with YOLOv8.
- **/[`results`](https://github.com/SShivamshan/Projet_MOOREV/tree/main/results) :** Storage of results obtained from analyses and experiments.

## 🛠 *Requirements*

Pip install [`requirements`](https://github.com/SShivamshan/Projet_MOOREV/blob/main/requirements.txt) in a Python>=3.8 environment with PyTorch>=1.8.

```bash
pip install --upgrade -r requirements.txt
```

## 💡 *How to Contribute*

1. Clone the repository locally: `git clone https://`[`github.com/your-username/repo-name`](https://github.com/SShivamshan/Projet_MOOREV)`.git`
2. Create your feature branch: `git checkout -b your-feature-name`
3. Make your changes and commit: `git commit -m "Added feature X"`
4. Push your changes to the branch: `git push origin your-feature-name`
5. Create a Pull Request to discuss the changes made.

We encourage any contributions, whether they be bug reports, new features, or improvements to the documentation.

## 🚀 *Run tools*

### Training
In order to train your own model, run the following command:
```bash
python train\main.py --names "class1,class2,class3" --nb_epoch 10 --nb_batch 8 --model_path path/to/model --dir path/to/directory --training_data path/to/training_data.zip --optimizer "adam" --lr0 0.001 --lrf 0.0001 --momentum 0.9 --seed 42
    --names                        # Comma-separated list of class names
    --nb_epoch                     # Number of epochs for training
    --nb_batch                     # Batch size for training
    --model_path                   # Path to the YOLOv8 model. If using the default model, specify "default".
    --dir                          # Directory where the model is stored
    --training_data                # Path to the training data zip file
    --optimizer                    # Optimizer for training (e.g., "adam")
    --lr0                          # Initial learning rate
    --lrf                          # Final learning rate
    --momentum                     # Momentum value
    --seed                         # Random seed for reproducibility
```

### Inference
In order to test the trained model on your local machine to segment, track on videos, and extract features of the species, run the following command:
```bash
python inference\main.py input_file model_path conf dir save_csv save_prediction save_annotation
   --input_file                   # Path to the input file. It could be an image or a video.
   --model_path                   # Path to the trained model. 
   --conf                         # Confidence in percentage.
   --dir                          # Directory of the model.
   --save_csv                     # True or False to specify whether to save the CSV file.
   --save_prediction              # True or False to specify whether to save predictions.
   --save_annotation              # True or False to specify whether to save annotations.
```

## ⌛ *Results*
### *Segmentation on images*
![Alt Text](results/segmentation on images.jpg)

### *Tracking on a video*

![Tracking actinia-equina](https://github.com/SShivamshan/Projet_MOOREV/blob/main/results/tracking%20actinia-equina.avi)

### *Annotation on [VIAME](https://viame.kitware.com/#/)*

![Annotation on VIAME](https://github.com/SShivamshan/Projet_MOOREV/blob/main/results/annotation%20on%20VIAME.avi)

### *Launch tools on [Galaxy-Ecology Europe](https://usegalaxy.eu/)*

![Launch tools on Galaxy](https://github.com/SShivamshan/Projet_MOOREV/blob/main/results/Launch%20tools%20on%20Galxy.mp4)

