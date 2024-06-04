from flask import Flask, send_file
from pydantic import BaseModel, ValidationError, field_validator
from lsystem import draw_lines, LFigure, LSystem2D
from io import BytesIO

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


# /l_system/iter=3,angle=90,axiom="F-F-F-F",prod={'F': 'F-F+F+F'}
@app.route("/l_system/<grammatic>")
def l_system(grammatic: str):
    try:
        grammatic_ = Grammatic.parse_obj(dict(el.split("=") for el in grammatic.split(",")))
        iter = grammatic_.iter
        angle = grammatic_.angle
        prod = grammatic_.prod
        axiom = grammatic_.axiom
        lsystem = LSystem2D(iter, angle, prod, axiom)
        figure = LFigure(lsystem, size=(1000, 1000))
        canvas = draw_lines(figure.lines)
        img_io = BytesIO()
        canvas.save(img_io, format='PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except ValidationError as e:
        result = "<ul>"
        for error in e.errors():
            result+= f"<li>{error}</li>"
        result += "</ul>"
        return result

@app.route('/test')
def test():
    black = (  0,   0,   0, 255)
    white = (255, 255, 255, 255)
    iter = 3
    angle = 90
    axiom = 'f'
    prod = {
        'f': 'F-[[f]+f]+F[+Ff]-f',
        'F': 'FF',
    }

    lsystem = LSystem2D(axiom, prod, iter, angle)
    figure = LFigure(lsystem, size=(1000, 1000))
    canvas = draw_lines(figure.lines)
    img_io = BytesIO()
    canvas.save(img_io, format='PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')
