from collections import deque


class HopcroftKarp:
    def __init__(self, graph):
        self.graph = graph
        self.left_nodes = list(graph.keys())
        self.pair_left = {u: None for u in self.left_nodes}

        right_nodes = set()
        for neighbours in graph.values():
            right_nodes.update(neighbours)

        self.right_nodes = list(right_nodes)
        self.pair_right = {v: None for v in self.right_nodes}
        self.distance = {}

    def bfs(self):
        queue = deque()
        found_free = False

        for u in self.left_nodes:
            if self.pair_left[u] is None:
                self.distance[u] = 0
                queue.append(u)
            else:
                self.distance[u] = float("inf")

        while queue:
            u = queue.popleft()

            for v in self.graph[u]:
                matched_u = self.pair_right[v]

                if matched_u is None:
                    found_free = True
                elif self.distance[matched_u] == float("inf"):
                    self.distance[matched_u] = self.distance[u] + 1
                    queue.append(matched_u)

        return found_free

    def dfs(self, u):
        for v in self.graph[u]:
            matched_u = self.pair_right[v]

            if matched_u is None or (
                self.distance[matched_u] == self.distance[u] + 1
                and self.dfs(matched_u)
            ):
                self.pair_left[u] = v
                self.pair_right[v] = u
                return True

        self.distance[u] = float("inf")
        return False

    def maximum_matching(self):
        matching = 0

        while self.bfs():
            for u in self.left_nodes:
                if self.pair_left[u] is None:
                    if self.dfs(u):
                        matching += 1

        return matching

    def get_matching(self):
        return self.pair_left