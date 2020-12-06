from pulp import LpProblem, LpMaximize, LpVariable, lpSum, PULP_CBC_CMD  # type: ignore


def my_print(string: str, verbose: bool) -> None:
    if verbose:
        print(string)


def helenas_triangles_solver(
    top_row_nodes: int, bottom_row_nodes: int, verbose: bool = True
):
    prob = LpProblem("Triangles", LpMaximize)
    assert top_row_nodes >= 1
    assert bottom_row_nodes >= 2
    assert top_row_nodes <= bottom_row_nodes

    # INIT EDGES

    # start with bottom left node, and conect it to all on top and
    # connect to the one on the right and all on
    # the top row. do the same for all on the bottom row
    # Then, connect every node on the top row with the one to the right

    edges = {}
    for btm in range(bottom_row_nodes):

        if btm < bottom_row_nodes - 1:
            vertices = ["B" + str(btm), "B" + str(btm + 1)]
            name = "_".join(vertices)
            lpVar = LpVariable(name, 0, 1, cat="Integer")
            edges[name] = {"var": lpVar, "vertices": vertices}
        for top in range(top_row_nodes):
            vertices = ["B" + str(btm), "T" + str(top)]
            name = "_".join(vertices)
            lpVar = LpVariable(name, 0, 1, cat="Integer")
            edges[name] = {"var": lpVar, "vertices": vertices}
    for top in range(top_row_nodes - 1):
        vertices = ["T" + str(top), "T" + str(top + 1)]
        name = "_".join(vertices)
        lpVar = LpVariable(name, 0, 1, cat="Integer")
        edges[name] = {"var": lpVar, "vertices": vertices}

    # INIT TRIANGLES

    triangles = {}
    for btm in range(bottom_row_nodes):
        # connect to next on bottom row and each of the ones on top
        if btm < bottom_row_nodes - 1:
            for top in range(top_row_nodes):
                vertices = ["B" + str(btm), "B" + str(btm + 1), "T" + str(top)]
                name = "_".join(vertices)
                lpVar = LpVariable(name, 0, 1, cat="Integer")
                triangles[name] = {"var": lpVar, "vertices": vertices}

        # connects to each pair of consecutive nodes on the top row
        for top in range(top_row_nodes - 1):
            vertices = ["B" + str(btm), "T" + str(top), "T" + str(top + 1)]
            name = "_".join(vertices)
            lpVar = LpVariable(name, 0, 1, cat="Integer")
            triangles[name] = {"var": lpVar, "vertices": vertices}

    def check_vertices_match(v_edge, v_tri):
        return v_edge[0] in v_tri and v_edge[1] in v_tri

    # OBJECTIVE

    triangle_var_list = [t["var"] for t in triangles.values()]
    prob += lpSum(triangle_var_list)

    # constraints

    for edge_val in edges.values():
        # get all triangles that have the same vertices
        vertices = edge_val["vertices"]
        triangles_to_contraint = []
        for tri in triangles.values():
            if check_vertices_match(vertices, tri["vertices"]):
                triangles_to_contraint.append(tri["var"])
        prob += edge_val["var"] == lpSum(triangles_to_contraint)

    # SOLVE

    prob.solve(PULP_CBC_CMD(msg=0))

    # PRINT
    my_print(f"TOTAL POSSIBLE EDGES:     {len(edges.keys())}", verbose)
    my_print(f"TOTAL POSSIBLE TRIANGLES: {len(triangles.keys())}", verbose)

    triangles_output = []
    edges_output = []

    tri_count = 0
    edge_count = 0
    for v in prob.variables():
        if v.name.count("_") == 2 and v.varValue == 1:
            # my_print(v.name," // " , v.varValue)
            tri_count += 1
            triangles_output.append(v.name)
        elif v.name.count("_") == 1 and v.varValue == 1:
            edge_count += 1
            edges_output.append(v.name)
    my_print(f"top {top_row_nodes} // bottom {bottom_row_nodes}", verbose)
    my_print(f"NUMBER OF TRIANGLES: {tri_count}", verbose)
    my_print(f"NUMBER OF EDGES:     {edge_count}", verbose)
    if tri_count == top_row_nodes + bottom_row_nodes - 2:
        my_print("BOTTOM + TOP - 2 RULE CHECKS OUT", verbose)
    elif tri_count == bottom_row_nodes - 1:
        my_print("BOTTOM - 1 RULE CHECKS OUT", verbose)
    elif tri_count == bottom_row_nodes // 2:
        my_print("BOTTOM INTEGER DIVISION BY 2 RULE CHECKS OUT", verbose)

    return {"edges": edges_output, "triangles": triangles_output}


helenas_triangles_solver(5, 6)
