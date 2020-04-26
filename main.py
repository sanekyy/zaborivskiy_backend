from flask import Flask, request, jsonify

from figure_approximator import approximate
from figure_generator import FigureGenerator, generate_triangle
from figure_recognizer import FigureRecognizer

from tessellation import tessellation

app = Flask(__name__)

figureRecognizer = FigureRecognizer()
figureGenerator = FigureGenerator()


@app.route("/")
def hello():
    FigureGenerator().save_square("./static/generated/image")
    return "Hello World!"


@app.route("/generateFigure")
def generate_figure():
    id = request.args.get('id', '')
    type = request.args.get('type', '')
    path = "/static/generated/{0}".format(id)

    if type == "1":
        figureGenerator.save_triangle("." + path)
    elif type == "2":
        figureGenerator.save_square("." + path)
    elif type == "3":
        figureGenerator.save_hexagon("." + path)

    return "http://localhost:5000" + path + ".png"


@app.route("/recognizeFigure")
def recognize_figure():
    id = request.args.get('id', '')
    path = "./static/generated/{0}.png".format(id)
    type = figureRecognizer.predict_figure(path)
    return str(type)


@app.route("/approximateFigure")
def approximate_figure():
    id = request.args.get('id', '')
    type = request.args.get('type', '')
    path = "static/generated/{0}.png".format(id)
    outputPath = "static/approximated/{0}.png".format(id)

    imageUrl = "http://localhost:5000/" + outputPath

    figure = []
    if type == "1":
        figure = approximate(filename=path, class_type=2, output_filename=outputPath)
    elif type == "2":
        figure = approximate(filename=path, class_type=1, output_filename=outputPath)
    elif type == "3":
        figure = approximate(filename=path, class_type=0, output_filename=outputPath)

    coordinates = figure[0].tolist()
    return jsonify(imageUrl=imageUrl, coordinates=coordinates, area=figure[1], perimeter=figure[2])


@app.route("/tessellateFigure", methods=['POST'])
def tessellate_figure():
    json = request.get_json()

    polygonVertices = json["polygonVertices"]
    figureVertices = json["figureVertices"]

    id = request.args.get('id', '')
    imagePath = "static/tessellation/{0}.png".format(id)
    imageUrl = "http://localhost:5000/" + imagePath

    result_figures, n_figures, area_prop = tessellation(polygonVertices, figureVertices, imagePath)

    return jsonify(imageUrl=imageUrl, figuresCount=n_figures, coverPercent=area_prop)


if __name__ == "__main__":
    app.run()
