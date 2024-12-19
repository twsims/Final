
import math
from geopy.distance import geodesic
import networkx as nx
import folium
import itertools

# True geographical coordinates for the schools
schools = {
    'American Canyon': (38.16758, -122.23883),
    'St Marys': (37.888308, -122.28354),
    'St Patrick': (38.08716, -122.20248),
    'Rodriguez': (38.19977, -122.14580),
    'Jesse Bethel': (38.12048, -122.20775),
    'Benicia': (38.06512, -122.17585),
    'FairField': (38.27802, -122.03089),
    'Vanden':(38.28229, -121.96281),
    'Salesian': (37.95316, -122.34087),
    'Napa': (38.31148, -122.29703),
    'Vintage':(38.33333, -122.30462),
    'St Helena':(38.49681, -122.46265),
    'College Prep': (37.84862, -122.23983),
    'Vallejo': (38.11600, -122.24595),
    'Petaluma': (38.22772, -122.64636),
    'Sonoma': (38.28270, -122.45788),
    'Albany': (37.89600, -122.29219),
    'Oakland Tech': (37.83252, -122.25455),
    'El Cerito': (37.90820, -122.29529),
    'Novato': (38.08944, -122.57322)
}

# Function to calculate geographical distance
def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).kilometers

# Create a weighted graph
graph = nx.Graph()

# Add nodes and edges with weights
for school1, coord1 in schools.items():
    graph.add_node(school1, pos=coord1)
    for school2, coord2 in schools.items():
        if school1 != school2:
            distance = calculate_distance(coord1, coord2)
            graph.add_edge(school1, school2, weight=distance)

# Find the shortest path between all pairs of schools
def find_all_shortest_paths(graph):
    paths = {}
    for school1, school2 in itertools.combinations(schools.keys(), 2):
        path = nx.shortest_path(graph, source=school1, target=school2, weight="weight")
        distance = nx.shortest_path_length(graph, source=school1, target=school2, weight="weight")
        paths[(school1, school2)] = (path, distance)
    return paths
# Compute the Minimum Spanning Tree (MST)
mst = nx.minimum_spanning_tree(graph, weight="weight")

# Visualize the MST on a map
def visualize_mst(schools, mst):
    # Create a folium map centered at the midpoint of the schools
    center_lat = sum(coord[0] for coord in schools.values()) / len(schools)
    center_lon = sum(coord[1] for coord in schools.values()) / len(schools)
    school_map = folium.Map(location=(center_lat, center_lon), zoom_start=10)

    # Add schools to the map
    for school, coord in schools.items():
        folium.Marker(location=coord, popup=school).add_to(school_map)

    # Add MST edges to the map
    for edge in mst.edges(data=True):
        school1, school2, data = edge
        start = schools[school1]
        end = schools[school2]
        distance = data["weight"]
        folium.PolyLine(
            [start, end],
            color="blue",
            weight=2.5,
            opacity=0.8,
            tooltip=f"{school1} -> {school2}: {distance:.2f} km"
        ).add_to(school_map)
        # Adding a midpoint marker for the edge with distance
        mid_lat = (start[0] + end[0]) / 2
        mid_lon = (start[1] + end[1]) / 2 
        folium.Marker(
            location=(mid_lat, mid_lon),
            icon=folium.DivIcon(
                httml=f'<div styles="font-size: 10pt; color: black;">{distance:.2f} km</div>'
            ),
        ).add_to(school_map)

def tournament_schedule(paths):
    schedule = []
    for (school1, school2), (path, distance) in paths.items():
        schedule.append({
            "match_up": f"{school1} vs {school2}",
            "path": " -> ".join(path),
            "distance": f"{distance:.2f} km"
        })
    return schedule #Makes sure the schedule is returend    
# Visualize all shortest paths on a map
def visualize_all_paths(schools, graph, paths):
    # Create a folium map centered at the midpoint of the schools
    center_lat = sum(coord[0] for coord in schools.values()) / len(schools)
    center_lon = sum(coord[1] for coord in schools.values()) / len(schools)
    school_map = folium.Map(location=(center_lat, center_lon), zoom_start=10)

    # Add schools to the map
    for school, coord in schools.items():
        folium.Marker(location=coord, popup=school).add_to(school_map)

    # Add each path to the map
    for (school1, school2), (path, distance) in paths.items():
        for i in range(len(path) - 1):
            start = schools[path[i]]
            end = schools[path[i + 1]]
            folium.PolyLine(
                [start, end],
                color="blue",  # You can randomize this for different colors
                weight=2.5,
                opacity=0.8,
                tooltip=f"{school1} -> {school2}: {distance:.2f} km"
            ).add_to(school_map)

def visualize_mst_with_weights(schools, mst):
    # Create a folium map centered at the midpoint of the schools
    center_lat = sum(coord[0] for coord in schools.values()) / len(schools)
    center_lon = sum(coord[1] for coord in schools.values()) / len(schools)
    school_map = folium.Map(location=(center_lat, center_lon), zoom_start=10)

    # Add schools to the map
    for school, coord in schools.items():
        folium.Marker(location=coord, popup=school).add_to(school_map)

    # Add MST edges to the map with distances
    for edge in mst.edges(data=True):
        school1, school2, data = edge
        start = schools[school1]
        end = schools[school2]
        distance = data["weight"]
        folium.PolyLine(
            [start, end],
            color="blue",
            weight=2.5,
            opacity=0.8,
            tooltip=f"{school1} -> {school2}: {distance:.2f} km"
        ).add_to(school_map)

        # Add a midpoint marker for the edge with the distance
        mid_lat = (start[0] + end[0]) / 2
        mid_lon = (start[1] + end[1]) / 2
        folium.Marker(
            location=(mid_lat, mid_lon),
            icon=folium.DivIcon(
                html=f'<div style="font-size: 10pt; color: black;">{distance:.2f} km</div>'
            ),
        ).add_to(school_map)


# Calculate all shortest paths
all_paths = find_all_shortest_paths(graph)
tournament_schedule_data = tournament_schedule(all_paths)

#Print tournament Schedule
print("Tournament Schedule:")
for match in tournament_schedule_data:
    print(f"{match['match_up']}: {match['path']} (Distance: {match['distance']})")

# Display the map with all shortest paths
#visualize_all_paths(schools, graph, all_paths)
print("Map saved as mst_map.html")

# Visualize the MST
#visualize_mst(schools, mst)
visualize_mst_with_weights(schools, mst)
