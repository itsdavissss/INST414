import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load and Clean Data
df = pd.read_csv("wikiRfA.csv")

# Remove any rows with missing values in key columns
df.dropna(subset=['SOURCE', 'TARGET', 'VOTE'], inplace=True)

# Ensure votes are valid (-1 = oppose, 0 = neutral, 1 = support)
df = df[df['VOTE'].isin([-1, 0, 1])]

# Create Directed, Signed Graph ---
G = nx.DiGraph()

# Add edges with signs (excluding neutral votes)
for index, row in df.iterrows():
    voter = row['SOURCE']
    candidate = row['TARGET']
    vote = row['VOTE']
    
    if vote != 0:  # Exclude neutral votes
        G.add_edge(voter, candidate, sign=vote)

largest_scc = max(nx.strongly_connected_components(G), key=len)
G_scc = G.subgraph(largest_scc).copy()

# Calculate Centrality Measures 
out_degree_centrality = nx.out_degree_centrality(G)  # Most active voters
eigenvector_centrality = nx.eigenvector_centrality(G_scc, weight=None)  # Most influential voters

# Display Top Voters
def display_top_voters(centrality, title, top_n=10):
    """Displays the top voters based on a given centrality measure."""
    top_voters = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]
    print(f"\nTop {top_n} {title}:")
    for voter, score in top_voters:
        print(f"Voter: {voter}, Score: {score:.4f}")

display_top_voters(out_degree_centrality, "Most Active Voters (Out-Degree)")
display_top_voters(eigenvector_centrality, "Most Influential Voters (Eigenvector)")

# Visualize Network: Top 50 Influential Voters 
top_eigenvector_voters = sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:20]
subset_voters = [voter for voter, _ in top_eigenvector_voters]
subset_G = G.subgraph(subset_voters)

# Node colors based on eigenvector centrality
node_colors = [eigenvector_centrality.get(voter, 0) for voter in subset_G.nodes()]

# Node sizes based on out-degree centrality
node_sizes = [out_degree_centrality.get(voter, 0) * 1000 for voter in subset_G.nodes()]

# Edge colors based on vote sign (green = support, red = oppose)
edge_colors = [('green' if data['sign'] == 1 else 'red') for _, _, data in subset_G.edges(data=True)]

# Layout for visualization
pos = nx.spring_layout(subset_G, k=0.15, iterations=20)

# Draw network
fig, ax = plt.subplots(figsize=(15, 10))
nx.draw_networkx_nodes(subset_G, pos, node_color=node_colors, node_size=node_sizes, cmap=plt.cm.viridis, ax=ax)
nx.draw_networkx_edges(subset_G, pos, edge_color=edge_colors, alpha=0.7, width=0.8, arrows=True, ax=ax)
nx.draw_networkx_labels(subset_G, pos, font_size=8, ax=ax)

# Add colorbar
sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=min(node_colors), vmax=max(node_colors)))
sm.set_array([])
plt.colorbar(sm, label="Eigenvector Centrality (Voter Influence)", ax=ax)

plt.title("Wikipedia RfA Network (Top 20 Most Influential Voters)")
plt.axis('off')
plt.show()