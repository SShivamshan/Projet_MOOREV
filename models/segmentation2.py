# main_script.py
import sys
from PIL import Image
from ultralytics import YOLO

use_cuda = False
model_path = "best.pt"
use_CPU = True
task = "segment"
save = False
show = False



def load_networks():
    if use_CPU :
        return YOLO(model_path)
    else:
        pass

def segmentation(input_images, result_images, conf):
    model = load_networks()
    results = model.predict(
        input_images,
        task = task,
        save = save ,
        show = show,
        conf = conf,
    )

    # Show the results
    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        im.show()  # show image
        im.save(result_images)  # save image


if __name__ == "__main__":

    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python segmentation.py <input image file> <output image file> <conf>")
        sys.exit(1)

    input_images = sys.argv[1]
    result_images = sys.argv[2]
    conf = float(sys.argv[3])

    # input_images = "data/images/image.jpg"
    # result_images = "data/images/result.jpg"

    segmentation(input_images, result_images, conf)
