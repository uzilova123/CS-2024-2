from flask import Flask, send_file
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
        try:
            return eval(raw)
        except SyntaxError as e:
            raise ValueError(f"Syntax Error: {e}")


@app.route("/l_system_file/<grammatic>")
def l_system_file(grammatic: str):
    return send_file(path_or_file="file/quadratic Koch island - 2.png")


# /l_system/it=3,angle=90,axiom="F-F-F-F",prod="{'F': 'F-F+F+F'}
@app.route("/l_system/<grammatic>")
def l_system(grammatic: str):
    try:
        grammatic_ = Grammatic.parse_obj(dict(el.split("=") for el in grammatic.split(",")))
        return (
            f'<p>{grammatic_}</p>'
            + f'<img src="/l_system_file/{grammatic}" alt="L-System" width="500" height="500">'
        )
    except ValidationError as e:
        result = "<ul>"
        for error in e.errors():
            result+= f"<li>{error}</li>"
        result += "</ul>"
        return result
