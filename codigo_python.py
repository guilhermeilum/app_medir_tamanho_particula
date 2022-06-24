import plotly
import plotly.express as px
import plotly.graph_objects as go
from skimage import measure,color,io
from os import path
from time import sleep
def area_particula(caminho_imagem):
    try:
        escala = float(input("digite o valor da esvala em \u03BCm por px: "))
    except(ValueError):
        print("valor não compreedido")
        sleep(0.5)
        return
    numero_padrao = input('valor da sensibilidade da lable, não é aconcelhado mudar o valor, para continuar somente clique no "enter". ')
    if len(numero_padrao) == 0: 
        numero_padrao = 0.56
    else: 
        try: 
            numero_padrao = float(numero_padrao)
        except(ValueError): 
            print("valor não compreedido")
            sleep(0.5)
            return
    file = path.join(caminho_imagem) 
    try:
        image = io.imread(file)
    except(FileNotFoundError):
        print("local não identificado")
        sleep(0.5)
        return
    print("Preparando a imagem, isso pode demorar alguns segundos ou minutos.")
    img= color.rgb2gray(image)
    mask = img < numero_padrao
    labels = measure.label(mask)
    fig = px.imshow(img, binary_string=True)
    fig.update_traces(hoverinfo='skip') # hover is only for label info

    props = measure.regionprops(labels, img)
    properties = ['area']

    # For each label, add a filled scatter trace for its contour,
    # and display the properties of the label in the hover of this trace.
    for index in range(1, labels.max()):
        label_i = props[index].label
        contour = measure.find_contours(labels == label_i, 0.5)[0]
        y, x = contour.T
        hoverinfo = ''
        escala_quadrada = escala**2
        unidade = "\u03BCm"
        for prop_name in properties:
            hoverinfo += f'<b>{prop_name}: {str(round(((getattr(props[index], prop_name))*escala_quadrada),2))+unidade}</b><br>'
        fig.add_trace(go.Scatter(
            x=x, y=y, name=label_i,
            mode='lines', fill='toself', showlegend=False,
            hovertemplate=hoverinfo, hoveron='points+fills'))

    plotly.io.show(fig)
area_particula(input("local da imagem: "))