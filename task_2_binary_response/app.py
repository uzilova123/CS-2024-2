from flask import Flask
from pydantic import BaseModel, ValidationError, field_validator

app = Flask(__name__)

class Grammatic(BaseModel):
    iter: int
    angle: int
    axiom: str
    prod: dict[str, str]

    @field_validator("prod", mode="before")
    @classmethod
    def transform(cls, raw: str) -> dict[str, str]:
        return eval(raw)


# /l_system?it=3,angle=90,axiom="F-F-F-F",prod="{'F': 'F-F+F+F'}
@app.route("/l_system/<grammatic>")
def hello_world(grammatic: str):
    try:
        grammatic_dict = dict(el.split("=") for el in grammatic.split(","))
        grammatic_ = Grammatic.parse_obj(dict(el.split("=") for el in grammatic.split(",")))
        return f"<p>{grammatic_}</p>"
    except ValidationError as e:
        result = "<ul>"
        for error in e.errors():
            result+= f"<li>{error}</li>"
        result += "</ul>"
        return result
