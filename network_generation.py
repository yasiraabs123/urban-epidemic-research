"""
Network Generation for Three City Types
Student: Akhmetov Iskandar
Group: J4132
Course: Applied Mathematics and Computer Science
"""

import networkx as nx
import numpy as np
import pickle
import os

print("=" * 60)
print("NETWORK GENERATION FOR URBAN EPIDEMIC MODELING")
print("Student: Akhmetov Iskandar, Group J4132")
print("=" * 60)

# Create data directory
os.makedirs('data/networks', exist_ok=True)

def create_dense_city(n=50000):
    """Create dense mixed-use city network (scale-free)"""
    print("\n[1/3] Creating Dense City Network...")
    
    # Create scale-free network
    G = nx.barabasi_albert_graph(n, m=3)
    
    # Calculate metrics
    degrees = [d for n, d in G.degree()]
    avg_degree = np.mean(degrees)
    clustering = nx.average_clustering(G)
    
    print(f"   • Nodes: {n:,}")
    print(f"   • Edges: {G.number_of_edges():,}")
    print(f"   • Avg. Degree: {avg_degree:.1f}")
    print(f"   • Clustering: {clustering:.3f}")
    
    return G, avg_degree, clustering

def create_sparse_city(n=50000):
    """Create sparse segregated city network (modular)"""
    print("\n[2/3] Creating Sparse City Network...")
    
    # Create modular network
    num_communities = 100
    community_size = n // num_communities
    
    G = nx.Graph()
    
    # Add nodes
    for i in range(n):
        G.add_node(i)
    
    # Add edges within communities
    for comm in range(num_communities):
        start = comm * community_size
        end = (comm + 1) * community_size
        community_nodes = list(range(start, end))
        
        # Connect each node to 10 others in community
        for i in community_nodes:
            connections = np.random.choice(community_nodes, size=10, replace=False)
            for j in connections:
                if i != j:
                    G.add_edge(i, j)
    
    # Add few connections between communities
    for _ in range(1000):
        comm1, comm2 = np.random.choice(num_communities, 2, replace=False)
        node1 = np.random.randint(comm1 * community_size, (comm1 + 1) * community_size)
        node2 = np.random.randint(comm2 * community_size, (comm2 + 1) * community_size)
        G.add_edge(node1, node2)
    
    # Calculate metrics
    degrees = [d for n, d in G.degree()]
    avg_degree = np.mean(degrees)
    clustering = nx.average_clustering(G)
    
    print(f"   • Nodes: {n:,}")
    print(f"   • Edges: {G.number_of_edges():,}")
    print(f"   • Avg. Degree: {avg_degree:.1f}")
    print(f"   • Clustering: {clustering:.3f}")
    print(f"   • Communities: {num_communities}")
    
    return G, avg_degree, clustering

def create_polycentric_city(n=50000):
    """Create polycentric city network (small-world with hubs)"""
    print("\n[3/3] Creating Polycentric City Network...")
    
    # Create small-world network
    G = nx.watts_strogatz_graph(n, k=5, p=0.3)
    
    # Add 5 hub nodes
    hubs = np.random.choice(n, size=5, replace=False)
    
    # Connect each node to nearest hub
    for node in range(n):
        if node not in hubs:
            distances = [abs(node - hub) for hub in hubs]
            closest_hub = hubs[np.argmin(distances)]
            G.add_edge(node, closest_hub)
    
    # Connect hubs to each other
    for i in range(5):
        for j in range(i + 1, 5):
            G.add_edge(hubs[i], hubs[j])
    
    # Calculate metrics
    degrees = [d for n, d in G.degree()]
    avg_degree = np.mean(degrees)
    clustering = nx.average_clustering(G)
    
    print(f"   • Nodes: {n:,}")
    print(f"   • Edges: {G.number_of_edges():,}")
    print(f"   • Avg. Degree: {avg_degree:.1f}")
    print(f"   • Clustering: {clustering:.3f}")
    print(f"   • Hubs: {5}")
    
    return G, avg_degree, clustering

def save_network(G, filename, metrics):
    """Save network and metrics"""
    # Save as simple format (smaller file)
    with open(f"data/networks/{filename}.pkl", 'wb') as f:
        pickle.dump({
            'graph': G,
            'metrics': metrics
        }, f)
    
    print(f"   ✓ Saved: data/networks/{filename}.pkl")
    return True

# Generate all networks
if __name__ == "__main__":
    print(f"\nGenerating synthetic networks (n=50,000 each)...")
    
    # Create networks
    G_dense, deg_dense, clust_dense = create_dense_city(5000)  # Reduced for speed
    G_sparse, deg_sparse, clust_sparse = create_sparse_city(5000)
    G_poly, deg_poly, clust_poly = create_polycentric_city(5000)
    
    # Save networks
    save_network(G_dense, "dense_city", 
                 {"avg_degree": deg_dense, "clustering": clust_dense})
    save_network(G_sparse, "sparse_city", 
                 {"avg_degree": deg_sparse, "clustering": clust_sparse})
    save_network(G_poly, "polycentric_city", 
                 {"avg_degree": deg_poly, "clustering": clust_poly})
    
    # Summary table
    print("\n" + "=" * 60)
    print("SUMMARY: NETWORK METRICS")
    print("=" * 60)
    print(f"{'City Type':<15} {'Avg. Degree':<12} {'Clustering':<12}")
    print("-" * 40)
    print(f"{'Dense':<15} {deg_dense:<12.1f} {clust_dense:<12.3f}")
    print(f"{'Sparse':<15} {deg_sparse:<12.1f} {clust_sparse:<12.3f}")
    print(f"{'Polycentric':<15} {deg_poly:<12.1f} {clust_poly:<12.3f}")
    print("=" * 60)
    
    print("\n✅ Task 2 COMPLETED: All networks generated successfully!")
    print("Files saved in: data/networks/")