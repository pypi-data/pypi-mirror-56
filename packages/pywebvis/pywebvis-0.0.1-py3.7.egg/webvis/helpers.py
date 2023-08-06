import multiprocessing.dummy as thr
try:
    import matplotlib.pyplot as plt
    import mpld3
except Exception as e:
    print(e)
try:
    import seaborn as sns
    sns.set()
except Exception as e:
    print(e)


def threaded(f,*args):
    p = thr.Process(target=(f),args = args)
    p.start()
    return p

def get_mpl_html(value, config=None):
    fig, ax = plt.subplots()
    try:
        ax.plot( value )
    except Exception as e:
        return str(e)
    s = mpld3.fig_to_html(fig)
    plt.close(fig)
    return s


