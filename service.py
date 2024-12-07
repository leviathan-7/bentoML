from __future__ import annotations

import io
import os
import bentoml
import base64
from PIL import Image

@bentoml.service(resources={"gpu": 1})
class YoloV8:
    def __init__(self):
        from ultralytics import YOLO
        yolo_model = os.getenv("YOLO_MODEL", "best.pt")
        self.model = YOLO(yolo_model)

    @bentoml.api
    def render(self, image_base64: str) -> str:
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes))
        result = self.model.predict(image)[0]
        save_file = "file.jpg"
        result.save(save_file)
        with open(save_file, "rb") as f:
            output_base64 = base64.b64encode(f.read())
        os.remove(save_file)
        return output_base64.decode('utf-8')
