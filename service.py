from __future__ import annotations

import json
import os
import typing as t
from pathlib import Path
import bentoml
from bentoml.validators import ContentType
from fastapi import FastAPI
from fastapi.responses import JSONResponse

Image = t.Annotated[Path, ContentType("image/*")]

@bentoml.service(resources={"gpu": 1})
class YoloV8:
    def __init__(self):
        from ultralytics import YOLO
        yolo_model = os.getenv("YOLO_MODEL", "best.pt")
        self.model = YOLO(yolo_model)

    @bentoml.api
    def render(self, image: Image) -> Image:
        result = self.model.predict(image)[0]
        output = image.parent.joinpath(f"{image.stem}_result{image.suffix}")
        result.save(str(output))
        return output
