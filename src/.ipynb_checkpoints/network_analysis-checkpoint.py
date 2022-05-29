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
# > Gather files in directory
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
    # Clear plot
    plt.clf()
    
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
    ap.add_argument("-i", "--input", required=True, help="Input data for the script - either a file or directory")
    # Parse argument
    arg = vars(ap.parse_args())
    # return list of argumnets 
    return arg
    
#=====> Define main()
def main(): 
    # Define user input
    user_input = parse_arg()["input"]
    
    # Print info
    print("[INFO] Drawing networks...")
    
    # If the user input is a single file
    if re.search("\.csv$", user_input):
        # Get filename
        file = user_input
        # Load graph-object
        G = load_net(file)
        # Create figure
        save_figure(G, file[:-4])
        # Get centrality scores
        centrality_scores(G, file[:-4])
    
    # if user input is a directory
    else: 
        # Gather files in directory
        file_list = gather_files(user_input)
    
        # Iterate over files
        for file in tqdm(file_list):
            # Load graph-object
            G = load_net(f"{user_input}/{file}")
            # Create figure
            save_figure(G, file[:-4])
            # Get centrality scores
            centrality_scores(G, file[:-4])
    
    # Print info
    print("[INFO] Job complete")

# Run main() function from terminal only
if __name__ == "__main__":
    main()
    
