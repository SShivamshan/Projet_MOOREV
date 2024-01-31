from kwiver.vital.algo import ImageObjectDetector

from kwiver.vital.types import Image
from kwiver.vital.types import ImageContainer
from kwiver.vital.types import DetectedObject
from kwiver.vital.types import DetectedObjectSet
from kwiver.vital.types import BoundingBoxD
import numpy as np
class speciesDetector( ImageObjectDetector ):
    """
    Implementation of ImageObjectDetector class
    """
    def __init__(self):
        ImageObjectDetector.__init__(self)

        # kwiver configuration variables
        self._kwiver_config = {
            'deployed': "",
            'thresh': 0.01,
            'xpu': "0",
            'batch_size': "auto",
            'input_string': ""
        }

        # netharn variables
        self._thresh = None
        self.predictor = None

    def get_configuration(self):
        # Inherit from the base class
        cfg = super(ImageObjectDetector, self).get_configuration()
        for key, value in self._kwiver_config.items():
            cfg.set_value(key, str(value))
        return cfg

    def set_configuration(self, cfg_in):
        cfg = self.get_configuration()

        # Imports used across this func
        import os
        import torch
        from bioharn import detect_predict

        # HACK: merge config doesn't support dictionary input
        _vital_config_update(cfg, cfg_in)

        for key in self._kwiver_config.keys():
            self._kwiver_config[key] = str(cfg.get_value(key))
        self._kwiver_config['thresh'] = float(self._kwiver_config['thresh'])

        self._thresh = float(self._kwiver_config['thresh'])

        if self._kwiver_config['batch_size'] == "auto":
            self._kwiver_config['batch_size'] = 2

            if torch.cuda.is_available():
                gpu_mem = 0
                if len(self._kwiver_config['xpu']) == 1 and \
                  self._kwiver_config['xpu'] != 0:
                    gpu_id = int(self._kwiver_config['xpu'])
                    gpu_mem = torch.cuda.get_device_properties(gpu_id).total_memory
                else:
                    self._gpu_count = torch.cuda.device_count()
                    for i in range( self._gpu_count ):
                        single_gpu_mem = torch.cuda.get_device_properties(i).total_memory
                    if gpu_mem == 0:
                        gpu_mem = single_gpu_mem
                    else:
                        gpu_mem = min(gpu_mem, single_gpu_mem)
                if gpu_mem > 9e9:
                    self._kwiver_config['batch_size'] = 4
                elif gpu_mem >= 7e9:
                    self._kwiver_config['batch_size'] = 3

        if os.name == 'nt':
            os.environ["KWIMAGE_DISABLE_TORCHVISION_NMS"] = "1"

        pred_config = detect_predict.DetectPredictConfig()
        pred_config['batch_size'] = self._kwiver_config['batch_size']
        pred_config['deployed'] = self._kwiver_config['deployed']
        if torch.cuda.is_available():
            pred_config['xpu'] = self._kwiver_config['xpu']
        else:
            pred_config['xpu'] = "cpu"
        self.predictor = detect_predict.DetectPredictor(pred_config)

        self.predictor._ensure_model()
        return True

    def check_configuration(self, cfg):
        if not cfg.has_value("deployed"):
            print("A network deploy file must be specified!")
            return False
        return True

    def detect(self, image_data):
        full_rgb = image_data.asarray().astype('uint8')

        if len(self._kwiver_config['input_string']) > 0:
            dict_or_image = {self._kwiver_config['input_string']:full_rgb}
        else:
            dict_or_image = full_rgb

        predictor = self.predictor
        detections = predictor.predict(dict_or_image)

        # apply threshold
        flags = detections.scores >= self._thresh
        detections = detections.compress(flags)

        # convert to kwiver format
        output = _kwimage_to_kwiver_detections(detections)
        return output
def _vital_config_update(cfg, cfg_in):
    """
    Treat a vital Config object like a python dictionary

    Args:
        cfg (kwiver.vital.config.config.Config): config to update
        cfg_in (dict | kwiver.vital.config.config.Config): new values
    """
    # vital cfg.merge_config doesnt support dictionary input
    if isinstance(cfg_in, dict):
        for key, value in cfg_in.items():
            if cfg.has_value(key):
                cfg.set_value(key, str(value))
            else:
                raise KeyError('cfg has no key={}'.format(key))
    else:
        cfg.merge_config(cfg_in)
    return cfg


def _kwiver_to_kwimage_detections(detected_objects):
    """
    Convert vital detected object sets to kwimage.Detections

    Args:
        detected_objects (kwiver.vital.types.DetectedObjectSet)

    Returns:
        kwimage.Detections
    """
    import ubelt as ub
    import kwimage
    boxes = []
    scores = []
    class_idxs = []

    classes = []
    if len(detected_objects) > 0:
        obj = ub.peek(detected_objects)
        classes = obj.type.all_class_names()

    for obj in detected_objects:
        box = obj.bounding_box
        tlbr = [box.min_x(), box.min_y(), box.max_x(), box.max_y()]
        score = obj.confidence
        cname = obj.type.get_most_likely_class()
        cidx = classes.index(cname)
        boxes.append(tlbr)
        scores.append(score)
        class_idxs.append(cidx)

    dets = kwimage.Detections(
        boxes=kwimage.Boxes(np.array(boxes), 'tlbr'),
        scores=np.array(scores),
        class_idxs=np.array(class_idxs),
        classes=classes,
    )
    return dets


def _kwimage_to_kwiver_detections(detections):
    """
    Convert kwimage detections to kwiver deteted object sets

    Args:
        detected_objects (kwimage.Detections)

    Returns:
        kwiver.vital.types.DetectedObjectSet
    """
    from kwiver.vital.types.types import ImageContainer, Image

    segmentations = None
    # convert segmentation masks
    if 'segmentations' in detections.data:
        segmentations = detections.data['segmentations']

    boxes = detections.boxes.to_tlbr()
    scores = detections.scores
    class_idxs = detections.class_idxs

    if not segmentations:
        # Placeholders
        segmentations = (None,) * len(boxes)

    # convert to kwiver format, apply threshold
    detected_objects = DetectedObjectSet()

    for tlbr, score, cidx, seg in zip(boxes.data, scores, class_idxs, segmentations):
        class_name = detections.classes[cidx]

        bbox_int = np.round(tlbr).astype(np.int32)
        bounding_box = BoundingBoxD(
            bbox_int[0], bbox_int[1], bbox_int[2], bbox_int[3])

        detected_object_type = DetectedObjectType(class_name, score)
        detected_object = DetectedObject(
            bounding_box, score, detected_object_type)
        if seg:
            mask = seg.to_relative_mask().numpy().data
            detected_object.mask = ImageContainer(Image(mask))

        detected_objects.add(detected_object)
    return detected_objects

def __vital_algorithm_register__():
    from kwiver.vital.algo import algorithm_factory

    # Register Algorithm
    implementation_name = "species"

    if algorithm_factory.has_algorithm_impl_name(
      speciesDetector.static_type_name(), implementation_name ):
        return

    algorithm_factory.add_algorithm( implementation_name,
      "species dection inference routine", speciesDetector )

    algorithm_factory.mark_algorithm_as_loaded( implementation_name )