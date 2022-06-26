import plotly
import plotly.express as px
import plotly.graph_objects as go
from skimage import measure,color,io
from os import path
def area_particula(caminho_imagem):
    lista_area =[]
    file = path.join(caminho_imagem) 
    try:
        image = io.imread(file)
    except(FileNotFoundError):
        print("local não identificado")
        return None
    escala = 0
    while escala ==0:
        escala = escala_função()
    numero_padrao = 0
    while numero_padrao == 0:
        numero_padrao = numero_padrao_correto()
    print("Preparando a imagem, isso pode demorar alguns segundos ou minutos.")
    labels, fig, props = tratamento_da_imagem(image, numero_padrao)

    # For each label, add a filled scatter trace for its contour,
    # and display the properties of the label in the hover of this trace.
    for index in range(1, labels.max()):
        label_i = props[index].label
        contour = measure.find_contours(labels == label_i, 0.5)[0]
        y, x = contour.T
        hoverinfo = ''
        escala_quadrada = escala**2
        unidade = "\u03BCm²"
        area = round(((getattr(props[index], "area"))*escala_quadrada),2)
        lista_area.append(area)
        hoverinfo += f'<b>{"area"}: {str(area)+unidade}</b><br>'
        fig.add_trace(go.Scatter(
            x=x, y=y, name=label_i,
            mode='lines', fill='toself', showlegend=False,
            hovertemplate=hoverinfo, hoveron='points+fills'))

    plotly.io.show(fig)

def tratamento_da_imagem(image, numero_padrao):
    img= color.rgb2gray(image)
    mask = img < numero_padrao
    labels = measure.label(mask)
    fig = px.imshow(img, binary_string=True)
    fig.update_traces(hoverinfo='skip') # hover is only for label info
    props = measure.regionprops(labels, img)
    return labels,fig,props

def escala_função():
    try:
        escala = float(input("digite o valor da esvala em \u03BCm por px: "))
    except(ValueError):
        print("valor não compreendido")
    return escala

def numero_padrao_correto():
    numero_padrao = input('valor da sensibilidade da lable, não é aconcelhado mudar o valor, para continuar somente clique no "enter". ')
    if len(numero_padrao) == 0: 
        numero_padrao = 0.56
    else:
        try: 
            numero_padrao = float(numero_padrao)
        except(ValueError): 
            print("valor não compreendido")
            numero_padrao = 0
    return numero_padrao

area_particula(input("local da imagem: "))