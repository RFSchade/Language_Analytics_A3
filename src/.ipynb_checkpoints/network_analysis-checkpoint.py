#=====================================================#
#=============> Network Analysis Script <=============#
#=====================================================#

#=====> Import modules
# System tools
import os

# Data analysis
import pandas as pd
from collections import Counter
from itertools import combinations 
from tqdm import tqdm

# Network analysis tools
import networkx as nx
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,20)

# Regular expressions 
import re

# Parsing Arguments
import argparse

# User experience
from tqdm import tqdm

#====> Define functions
# > Am I inputting a directory or a csv file? Either way, save to list
def gather_files(user_input):
    path_to_dir = os.path.join("in", user_input)
    file_list = os.listdir(path_to_dir)
    return file_list

# > Load network
def load_net(filename):
    # Get the filepath
    filepath = os.path.join("in", filename)
    # Reading the filepath 
    data = pd.read_csv(filepath, sep='\t')
    G = nx.from_pandas_edgelist(data, "Source", "Target", ["Weight"])
    return G

# > Save figure 
def save_figure(G, filename):
    # Draw figure 
    nx.draw_networkx(G, with_labels=True, node_size=20, font_size=10)
    # Define outpath
    outpath = os.path.join('output', f'{filename}_net.png')
    # Save figure 
    plt.savefig(outpath, dpi=100, bbox_inches="tight")
    
# > Get Centrality scores
def centrality_scores(G, filename):
    # Finding degrees and creating dataframe 
    degrees = G.degree()
    df = pd.DataFrame(degrees, columns = ["names", "degrees"])
    # Finding and adding betweenness centrality 
    bc = nx.betweenness_centrality(G)
    df["betweenness"] = bc.values()
    # Finding and adding eigrnvector centrality
    ev = nx.eigenvector_centrality(G)
    df["eigenvector"] = ev.values()
    # Saving the dataframe
    outpath = os.path.join("output", f"{filename}_df.csv")
    df.to_csv(outpath, index=False)
    
# > Parse Argument
def parse_arg(): 
    # Initialize argparse
    ap = argparse.ArgumentParser()
    # Commandline parameters 
    ap.add_argument("-i", "--input", required=True, help="file or directory to be analyzed")
    # Parse argument
    arg = vars(ap.parse_args())
    # return list of argumnets 
    return arg
    
#=====> Define main()
def main(): 
    user_input = parse_arg()["input"]
    
    if re.search("\.csv$", user_input):
        file = user_input
        G = load_net(file)
        save_figure(G, file[:-4])
        centrality_scores(G, file[:-4])
        
    else: 
        file_list = gather_files(user_input)
    
        for file in tqdm(file_list):
            G = load_net(f"{user_input}/{file}")
            save_figure(G, file[:-4])
            centrality_scores(G, file[:-4])

# Run main() function from terminal only
if __name__ == "__main__":
    main()
    
# To be tested!