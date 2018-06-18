import matplotlib.pyplot as plt 
from graph_tool.all import *
from owlready import *

onto_path.append("/media/sheetal/New Volume/Major Project/Newspaper Ontology")
base_irri = 'http://aaa-mp.org/'

def generate_graph(onto):
    g = Graph(directed=False)
    g.vp.labels = g.new_vertex_property('string')
    g.vp.colors = g.new_vertex_property('vector<float>')
    g.ep.labels = g.new_edge_property('string')
    
    instances = onto.instances
    num_instances = len(instances)
    vertex_dict = {}
    
    for instance in onto.instances_of(onto.Event):
        v = g.add_vertex(1)
        i = int(v)
        g.vp.labels[i] = str(instance)
        g.vp.colors[i] = [0., 1., 0., 0.6]
        vertex_dict[str(instance)] = i
    
    for instance in onto.instances_of(onto.Entity):
        v = g.add_vertex(1)
        i = int(v)
        g.vp.labels[i] = str(instance)
        g.vp.colors[i] = [1., 0., 0., 0.6]
        vertex_dict[str(instance)] = i
        for event in instance.is_associated_with:
            g.add_edge(vertex_dict[str(event)], i)

    for instance in onto.instances_of(onto.Entity):
        i = vertex_dict[str(instance)]
        for action in instance.action:
            j = vertex_dict[str(action)]
            g.vp.colors[j] = [1., 1., 1., 1]
            g.add_edge(i, j)
            edge = g.edge(i, j)
            g.ep.labels[edge] = 'REL'

    L = int(g.add_vertex(1))
    g.vp.labels[L] = 'LOC'
    g.vp.colors[L] = [0., 0., 0., 1]

    P = int(g.add_vertex(1))
    g.vp.labels[P] = 'PER'
    g.vp.colors[P] = [0., 0., 0., 1]

    O = int(g.add_vertex(1))
    g.vp.labels[O] = 'ORG'
    g.vp.colors[O] = [0., 0., 0., 1]

    I = int(g.add_vertex(1))
    g.vp.labels[I] = 'IMG'
    g.vp.colors[I] = [0., 0., 0., 1]

    for instance in onto.instances_of(onto.Event):
        i = vertex_dict[str(instance)]
        for subjects in instance.subjects:
            j = vertex_dict[str(subjects)]
            edge = g.edge(i, j)
            g.ep.labels[edge] = 'OTHERS'
        for location in instance.location:
            j = vertex_dict[str(location)]
            edge = g.edge(i, j)
            g.ep.labels[edge] = 'LOC'
            if not g.edge(j, L):
                g.add_edge(j, L)
        for person in instance.person:
            j = vertex_dict[str(person)]
            edge = g.edge(i, j)
            g.ep.labels[edge] = 'PER'
            if not g.edge(j, P):
                g.add_edge(j, P)
        for org in instance.org:
            j = vertex_dict[str(org)]
            edge = g.edge(i, j)
            g.ep.labels[edge] = 'ORG'
            if not g.edge(j, O):
                g.add_edge(j, O)
        for image in instance.image:
            j = vertex_dict[str(image)]
            edge = g.edge(i, j)
            g.ep.labels[edge] = 'IMG'
            if not g.edge(j, I):
                g.add_edge(j, I)
        

    for instance in onto.instances_of(onto.Relevance):
        source = instance.source[0]
        dest = instance.dest[0]
        source_index = vertex_dict[str(source)]
        dest_index = vertex_dict[str(dest)]
        edge = g.edge(source_index, dest_index)
        g.ep.labels[edge] = instance.weight
        # print(instance.weight)
         
    return g
    
onto = get_ontology(base_irri+'news_onto.owl').load()
g = generate_graph(onto)
graph_draw(g, vertex_text=g.vp.labels, vertex_fill_color=g.vp.colors, vertex_font_size=10, edge_text=g.ep.labels, edge_font_size=10, output_size=(1920,1080), vertex_text_position=0)