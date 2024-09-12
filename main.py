import networkx as nx
import matplotlib.pyplot as plt
import math


class BuildingNavigator:
    def __init__(self):
        self.building_graph = nx.Graph()
        self.floors = {}
        self.coordinates = {}  # To store the (x, y) coordinates of nodes

    def add_location(self, location_name, floor, x, y):
        """Add a location (node) to the building graph, associated with a specific floor and coordinates."""
        node_id = f"{location_name}_F{floor}"
        self.building_graph.add_node(node_id, floor=floor, pos=(x, y))

        # Save coordinates for visualization
        self.coordinates[node_id] = (x, y)

        if floor not in self.floors:
            self.floors[floor] = []
        self.floors[floor].append(node_id)

    def calculate_distance(self, node1, node2):
        """Calculate Euclidean distance between two nodes based on their coordinates."""
        x1, y1 = self.coordinates[node1]
        x2, y2 = self.coordinates[node2]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def add_path(self, from_location, to_location, from_floor, to_floor):
        """Add a path (edge) between two locations on possibly different floors, and calculate the distance as weight."""
        from_node_id = f"{from_location}_F{from_floor}"
        to_node_id = f"{to_location}_F{to_floor}"

        # Calculate the weight (distance) between the two nodes
        distance = self.calculate_distance(from_node_id, to_node_id)

        # Add an edge with the distance as the weight
        self.building_graph.add_edge(from_node_id, to_node_id, weight=distance)

    def visualize_path(self, start_location, start_floor, end_location, end_floor):
        """Visualize the nodes and edges for each floor with the path to the destination in green."""
        start_node_id = f"{start_location}_F{start_floor}"
        end_node_id = f"{end_location}_F{end_floor}"

        # Compute the shortest path between start and end nodes
        try:
            shortest_path = nx.shortest_path(self.building_graph, source=start_node_id, target=end_node_id,
                                             weight='weight')
        except nx.NetworkXNoPath:
            print(f"No path found from {start_location} on floor {start_floor} to {end_location} on floor {end_floor}.")
            return

            # Get the edges that are part of the shortest path
        path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]

        # Group the path by floors
        floor_paths = {}
        for edge in path_edges:
            floor1 = self.building_graph.nodes[edge[0]]['floor']
            floor2 = self.building_graph.nodes[edge[1]]['floor']

            # If the edge is between the same floor, add it to that floor
            if floor1 == floor2:
                if floor1 not in floor_paths:
                    floor_paths[floor1] = []
                floor_paths[floor1].append(edge)
            else:
                # Handle edges between floors (e.g., staircases)
                if floor1 not in floor_paths:
                    floor_paths[floor1] = []
                floor_paths[floor1].append(edge)

        # Visualize each floor separately
        for floor, edges_on_floor in floor_paths.items():
            nodes_on_floor = self.floors.get(floor, [])
            subgraph = self.building_graph.subgraph(nodes_on_floor)

            # Extract positions for visualization
            pos = {node: self.coordinates[node] for node in nodes_on_floor}

            plt.figure(figsize=(8, 8))

            # Draw all nodes and edges (default black color)
            nx.draw(subgraph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10,
                    font_weight='bold', edge_color='black')

            # Highlight the path edges on this floor in green
            nx.draw_networkx_edges(subgraph, pos, edgelist=edges_on_floor, edge_color='green', width=3)


            plt.title(f"Path on Floor {floor}")
            plt.show()

navigator = BuildingNavigator()

# first floor nodes
navigator.add_location("Entrance", 1, x=0, y=0)
navigator.add_location("Corner 1", 1, x=0, y=-2)
navigator.add_location("Corner 2", 1, x=2, y=0)
navigator.add_location("Corner 3", 1, x=2, y=-2)
navigator.add_location("Corner 4", 1, x=6, y=0)
navigator.add_location("Corner 5", 1, x=6, y=-2)
navigator.add_location("Corner 6", 1, x=4, y=-2)
navigator.add_location("Corner 7", 1, x=4, y=-4)
navigator.add_location("Corner 8", 1, x=6, y=-4)

navigator.add_location("Room 101", 1, x=2, y=-1)
navigator.add_location("Room 102", 1, x=1, y=-2)
navigator.add_location("Room 103", 1, x=5, y=0)
navigator.add_location("Room 104", 1, x=5, y=-2)
navigator.add_location("Room 105", 1, x=5, y=-4)

navigator.add_location("Staircase Up", 1, x=3, y=0)

# second floor nodes
navigator.add_location("Corner 0", 2, x=0, y=0)
navigator.add_location("Corner 1", 2, x=0, y=-2)
navigator.add_location("Corner 2", 2, x=2, y=0)
navigator.add_location("Corner 3", 2, x=2, y=-2)
navigator.add_location("Corner 4", 2, x=6, y=0)
navigator.add_location("Corner 5", 2, x=6, y=-2)
navigator.add_location("Corner 6", 2, x=4, y=-2)
navigator.add_location("Corner 7", 2, x=4, y=-4)
navigator.add_location("Corner 8", 2, x=6, y=-4)

navigator.add_location("Room 201", 2, x=2, y=-1)
navigator.add_location("Room 202", 2, x=1, y=-2)
navigator.add_location("Room 203", 2, x=5, y=0)
navigator.add_location("Room 204", 2, x=5, y=-2)
navigator.add_location("Room 205", 2, x=5, y=-4)

navigator.add_location("Staircase Down", 2, x=3, y=0)

# first floor hallways

navigator.add_path("Entrance", "Corner 1", 1, 1)
navigator.add_path("Entrance", "Corner 2", 1, 1)
navigator.add_path("Corner 2", "Room 101", 1, 1)
navigator.add_path("Corner 3", "Room 101", 1, 1)
navigator.add_path("Corner 2", "Staircase Up", 1, 1)
navigator.add_path("Staircase Up", "Room 103", 1, 1)
navigator.add_path("Staircase Up", "Staircase Down", 1, 2)
navigator.add_path("Room 103", "Corner 4", 1, 1)
navigator.add_path("Corner 1", "Room 102", 1, 1)
navigator.add_path("Room 102", "Corner 3", 1, 1)
navigator.add_path("Corner 4", "Corner 5", 1, 1)
navigator.add_path("Corner 5", "Room 104", 1, 1)
navigator.add_path("Room 104", "Corner 6", 1, 1)
navigator.add_path("Corner 5", "Corner 8", 1, 1)
navigator.add_path("Corner 6", "Corner 3", 1, 1)
navigator.add_path("Corner 6", "Corner 7", 1, 1)
navigator.add_path("Corner 7", "Room 105", 1, 1)
navigator.add_path("Room 105", "Corner 8", 1, 1)

# second floor hallways

navigator.add_path("Corner 0", "Corner 1", 2, 2)
navigator.add_path("Corner 0", "Corner 2", 2, 2)
navigator.add_path("Corner 2", "Room 201", 2, 2)
navigator.add_path("Corner 3", "Room 201", 2, 2)
navigator.add_path("Corner 2", "Staircase Down", 2, 2)
navigator.add_path("Staircase Down", "Room 203", 2, 2)
navigator.add_path("Room 203", "Corner 4", 2, 2)
navigator.add_path("Corner 1", "Room 202", 2, 2)
navigator.add_path("Room 202", "Corner 3", 2, 2)
navigator.add_path("Corner 4", "Corner 5", 2, 2)
navigator.add_path("Corner 5", "Room 204", 2, 2)
navigator.add_path("Room 204", "Corner 6", 2, 2)
navigator.add_path("Corner 5", "Corner 8", 2, 2)
navigator.add_path("Corner 6", "Corner 3", 2, 2)
navigator.add_path("Corner 6", "Corner 7", 2, 2)
navigator.add_path("Corner 7", "Room 205", 2, 2)
navigator.add_path("Room 205", "Corner 8", 2, 2)

# navigator.add_location("Staircase Up", 2, x=1, y=0)
# navigator.add_location("Room 201", 2, x=1, y=1)
# navigator.add_location("Room 202", 2, x=2, y=1)
# navigator.add_location("Corner 2", 2, x=1, y=-1)
#
# # Visualize Floor 1
navigator.visualize_path("Entrance", 1, "Room 205", 2)
#
# # Visualize Floor 2
# navigator.visualize_floor(2)
