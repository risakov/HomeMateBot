import plotly.graph_objects as go
import pandas as pd
import numpy as np
import imageio

countries = ["US", "Spain", "Italy", "United Kingdom", "France", "Germany", "Russia", "Turkey", "Brazil", "Iran", "China"]

data = pd.read_csv(
    r"https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv", parse_dates=['Date'])

title = "Выздоровевших от коронавируса на"


def get_rgb_val():
    # r = np.random.randint(1, 255)
    r = np.random.randint(50, 100)
    g = 255
    b = np.random.randint(87, 128)
    return [r, g, b]


def make_figure(data, S):
    R = go.Figure(data=[go.Bar(x=data["names"], y=data["pop"],
                           marker_color=data["color"], text=data["names"],
                           hoverinfo="none", textposition="outside",
                           texttemplate="%{x}<br>%{y:s}", cliponaxis=False)],
              layout=go.Layout(
                  font={"size": 20},
                  width=1000,
                  height=1200,
                  xaxis={"showline": False, "tickangle": -90, "visible": False},
                  yaxis={"showline": False, "visible": False},
                  title=title + ' ' + S))
    return R


def gif_construct():
    dates = data.loc[:, 'Date']
    cntrs = data.loc[:, 'Country']

    colors = []
    for i in range(len(countries)):
        c = get_rgb_val()
        colors.append("rgb(" + str(c[0]) + "," + str(c[1]) + "," + str(c[2]) + ")")

    j = 0
    names = []
    conf = []
    images = []
    for i in range(len(dates)):
        if cntrs[i] in countries:
            if j < len(countries):
                names.append(cntrs[i])
                conf.append(data.loc[:, 'Recovered'][i])
                j += 1
            else:
                j = 0
                S = str(dates[i])

                df = pd.DataFrame({"names": names[-11:len(names)], "pop": conf[-11:len(names)], "color": colors})
                pdata = df.sort_values(by="pop").iloc[-10:, ]

                fig = make_figure(pdata, S)

                fig.write_image('./images/image.png')
                images.append(imageio.imread('./images/image.png'))
    for i in range(10):
        images.append(imageio.imread('./images/image.png'))
    imageio.mimwrite('./images/recovered.gif', images, fps=6)


gif_construct()
