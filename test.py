from helenas_triangles import helenas_triangles_solver


def test_top_is_2():
    top_nodes = 2
    for bottom_nodes in range(3, 11):
        assert (
            len(helenas_triangles_solver(top_nodes, bottom_nodes)["triangles"])
            == bottom_nodes - 1
        )


def test_top_is_1():
    top_nodes = 1
    for bottom_nodes in range(3, 11):
        assert (
            len(helenas_triangles_solver(top_nodes, bottom_nodes)["triangles"])
            == bottom_nodes // 2
        )


def test_top_is_3_or_more():
    for top_nodes in range(3, 10):
        for bottom_nodes in range(top_nodes, 11):
            assert (
                len(helenas_triangles_solver(top_nodes, bottom_nodes)["triangles"])
                == bottom_nodes + top_nodes - 2
            )
