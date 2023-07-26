from __future__ import annotations

from graphviz import Digraph, nohtml
import json
from .graph import Graph


class PertChart:
    def __init__(self, graph: Graph):
        self._graph: Graph = graph

    @property
    def graph(self):
        return self._graph

    @staticmethod
    def from_json(filename: str) -> PertChart:
        with open(filename, "r") as f:
            json_obj = json.load(f)
        return PertChart(graph=Graph.from_json(json_obj))

    def calculate_values(self) -> PertChart:
        for k in self._graph:
            if self._graph[k].id == "START":
                continue
            pred = self._graph[k]["pred"]

            if self._graph[k]["pred"][0].id == "START":  # no predecessor
                self._graph[k]["end"] = (
                    self._graph[k]["start"] + self._graph[k]["duration"]
                )

            elif len(pred) == 1:  # 1 predecessor
                key = self._graph[k]["pred"][0].id

                self._graph[k]["start"] = self._graph[key]["end"]  # EF of predecessor
                self._graph[k]["end"] = (
                    self._graph[k]["start"] + self._graph[k]["duration"]
                )

            elif len(pred) > 1:  # more than 1 predecessor
                key = pred[1].id.strip()
                ends = [
                    self._graph[p.id.strip()]["end"] for p in pred
                ]  # list comprehenssion
                self._graph[k]["start"] = max(ends)
                self._graph[k]["end"] = (
                    self._graph[k]["start"] + self._graph[k]["duration"]
                )
                # l = p1[pred[1]]['EF'] # for j in range(len(pred))
                # p1[k]['ES'] = max([p1[pred[j]['EF'] for j in range(len(pred)
        return self

    def calculate_critical_task(self) -> PertChart:
        ...

    def create_pert_chart(
        self, task_list, fill_color="grey93", line_color="blue"
    ) -> None:
        a = task_list
        # Graph Instance
        g = Digraph(
            "g", filename="PERT.gv", node_attr={"shape": "Mrecord", "height": ".1"}
        )

        # configurations
        fl_color = fill_color
        ln_color = line_color

        g.attr(rankdir="LR")
        g.attr("node", shape="record")

        # Nodes

        """# this works for input file having one tuple of task per line (cf. v0.3)
        for i in range(len(a)):
            if a[i][0] == "END":
                    continue
            g.node(a[i][0], 
                   nohtml('<f0>' + 
                          a[i][0] + 
                          ' |{' + a[i][1] + '|' + a[i][2] + '|' + a[i][3] + '}|<f2>' + 
                          a[i][4]), 
                   fillcolor=fill_color, 
                   style='filled',
                   color= line_color
                  )
        """

        for k in a:
            if a[k]["Tid"] == "END":
                continue
            g.node(
                a[k]["Tid"],
                nohtml(
                    "<f0>"
                    + a[k]["Tid"]
                    + " |{"
                    + str(a[k]["start"])
                    + "|"
                    + str(a[k]["duration"])
                    + "|"
                    + str(a[k]["end"])
                    + "}|<f2>"
                    + a[k]["responsible"]
                ),
                fillcolor=fl_color,
                style="filled",
                color=ln_color,
            )

        # Edges
        """
        g.edge('node0:f2', 'node4:f1') # connect edges with connetion points <f2> and <f1>
        g.edge('node0', 'node1')
        """

        """# this works for input file having one tuple of task per line (cf. v0.3)
        for i in a: # for rows in a
            #g.edge(i[3] + ':f2', i[0] + ':f0')
            if i[0] == "END":
                g.edge(i[5], "FINISH")
            else:
                g.edge(i[5], i[0])
        """
        for k in a:  # for task in json task list
            # g.edge(i[3] + ':f2', i[0] + ':f0')
            if a[k]["Tid"] == "END":
                predecessors = a[k]["pred"]
                if len(predecessors) > 1:
                    for task in predecessors:
                        g.edge(task.id, a[k]["Tid"])
                else:
                    g.edge(a[k]["pred"][0].id, "FINISH")
            elif a[k]["Tid"] != "START":
                predecessors = a[k]["pred"]
                if len(predecessors) > 1:
                    for task in predecessors:
                        g.edge(task.id, a[k]["Tid"])
                else:
                    g.edge(a[k]["pred"][0].id, a[k]["Tid"])
        print(g)
        g.view()
