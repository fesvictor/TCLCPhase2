import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import pathlib

def plot_semiannual_graph(name, data, category, plot_kind="overall", save=False, show=True, suffix=None, params=None):
    if isinstance(suffix,str):
        if suffix == "chinese":
            plt.rcParams["font.family"] = "simhei"
        else:
            plt.rcParams["font.family"] = "sans-serif"
    weeks = [i + 1 for i in range(0, len(data[list(data.keys())[0]][plot_kind]))]
    dpi = 96
    plt.figure(figsize=(1366/dpi,768/dpi), dpi=dpi)
    plt.gca().set_color_cycle(['green', 'red', 'blue', 'purple', 'yellow', 'gray', 'orange', 'magenta'])
    
    plt.xlabel("Week")
    plt.ylabel("Polarity")
    plt.xticks(weeks, ["W" + str((i % 5)) if i % 5 == 1 else str((i % 5)) for i in weeks])
    
    graph_title = name + " " + plot_kind
    
    plt.suptitle(graph_title, fontsize=20)
    for n in data:
        plt.plot(weeks, data[n][plot_kind], label=n)
        
    plt.legend()
    
    if save:
        root_dir = params['output_dir']
        graph_dir = "semiannual_plot"
        current_run_dir = params['start_year'] + "-" + params['start_month'] + "__" + params['end_year'] + "-" + params['end_month']
        endpath = os.path.join(root_dir, graph_dir, current_run_dir, category)
        
        pathlib.Path(endpath).mkdir(parents=True, exist_ok=True)
        filename =category + "_" + plot_kind
        if isinstance(suffix, str):
            filename += "_" + suffix
        filename += ".png"
        print(filename)
        plt.savefig(os.path.join(endpath, filename), dpi=dpi)
        
    if show:
        plt.show()
    
    plt.close('all')