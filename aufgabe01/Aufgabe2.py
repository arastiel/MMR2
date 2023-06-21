import csv

nodes_data = []
edges_data = []
with open('nodes.csv') as nodedata:
    csv_reader_object = csv.reader(nodedata, delimiter=",")
    for row in csv_reader_object:
        nodes_data.append(row)

with open('edges.csv') as edgesdata:
    csv_reader_object = csv.reader(edgesdata, delimiter=",")
    for row in csv_reader_object:
        edges_data.append(tuple(row))

print(nodes_data)
#print(edges_data)