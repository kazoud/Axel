import matplotlib.pyplot as plt

def interactiveOn():
    plt.ion()

def plot(x: list[float], y: list[float], xlabel: str, ylabel: str, title: str):
    fig, ax = plt.subplots()
    ax.plot(x,y)
    ax.set(xlabel= xlabel, ylabel= ylabel,
        title= title)
    ax.grid()
    plt.show()

#à revoir si c'est comme ça qu'on veut que ça marche ou bien si qt offre autre chose