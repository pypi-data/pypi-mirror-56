
"""
speckdreieck module, see http://pypi.python.org/pypi/speckdreieck
for the documentation.
"""
import requests 

from earcut import earcut 

def find_dominant_axis(vertices):
    """ 
    measures which axis has least variance and returns 0, 1, or 2 (x, y, z)
    so the 3D coordinates can be reduced to 2D 

    """
    xArray = [x[0] for x in vertices]
    yArray = [x[1] for x in vertices]
    zArray = [x[2] for x in vertices]

    xVariance = max(xArray) - min(xArray)
    yVariance = max(yArray) - min(yArray)
    zVariance = max(zArray) - min(zArray)
    allVars = [xVariance, yVariance, zVariance]
    return allVars.index(min(allVars))

    
def get_vertex_order(coord_list):
    """ returns the order of vertices to triangulate the polygon """
    vertices = [coord_list[i:i + 3] for i in range(0, len(coord_list), 3)]
    minimalAxes = find_dominant_axis(vertices)
    # reduce to one liner 
    for i in vertices:
        i.pop(minimalAxes)
    poly = [j for i in vertices for j in i]
    vertex_order = earcut(poly)    
    return vertex_order

def parse_vertices(vertex_array, props={}):
    """
    Takes an array of 3D vertices describing a planar surface,
    triangulates the vertices and unpacks them into a speckle mesh object 

    """
    no_vertices = len(vertex_array) // 3
    if no_vertices == 3:
        faces = [0, 0, 1, 2]
    elif no_vertices == 4:
        faces = [0, 0, 1, 2, 0, 2, 3, 0]
    else: 
        faces = get_vertex_order(verts)
        for i in range(len(faces)-3, -1, -3):
            faces.insert(i, 0)   
    speckle_mesh = {
        "type" : "Mesh",
        "vertices" : vertex_array,
        "faces" : faces,
        "properties" :  props
    }
    return speckle_mesh 


def new_stream(speckle_server, name, description=''):
    url = "https://{}/api/streams".format(speckle_server)
    payload = {"name": name, "description": description}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    return r.json()