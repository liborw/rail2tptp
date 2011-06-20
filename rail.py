# 
#  rail.py
#  Module containing description and parsing for rail format.
#  
#  Created by Libor Wagner on 2011-05-24.
#  Copyright 2011 Libor Wagner. All rights reserved.
# 
# Rail format:
#   Node type                   format
#   Connection:                 name - in out
#   Notice with signpost:       name | in out
#   Coupler with signpost:      name > in1 in2 out
#   Tournout with signpost:     name < in1 out1 out2
#   Input with signpost:        name I out
#   Output:                     name O in
#   Comment:                    #
NODE_KINDS = ['I', 'O', '-', '|', '>', '<']
INPUT, OUTPUT, CONNECTION, NOTICE, COUPLER, TOURNOUT = NODE_KINDS

def conjunction(lst):
    """Create conjunction from the list."""
    conj = " & ".join(lst)
    if len(lst) > 1:
        conj = "("+conj+")"
    return conj

def disjunction(lst):
    """Create dsjunction from the list."""
    conj = " | ".join(lst)
    if len(lst) > 1:
        conj = "("+conj+")"
    return conj

class Edge(object):
    """Graph edge"""
    def __init__(self, name, head_id, tail_id):
        super(Edge, self).__init__()
        self.name = name
        self.head_id = head_id
        self.tail_id = tail_id
    
    def __repr__(self):
        return 'Edge({0}, {1}, {2})'.format(self.name, self.head_id, self.tail_id)
    
    def merge(self, other):
        if other.head_id:
            self.head_id = other.head_id
        else:
            self.tail_id = other.tail_id

def negate(formula):
    if formula:
        if formula[0] == '~':
            return formula[1:]
        else:
            return '~' + formula
    else:
        return formula

class Node(object):
    """Graph node"""
    def __init__(self, name, kind, incoming, outgoing):
        super(Node, self).__init__()
        self.name = name
        self.kind = kind
        self.incoming = incoming
        self.outgoing = outgoing
    
    def __repr__(self):
        incoming = '[' + ', '.join(self.incoming) + ']'
        outgoing = '[' + ', '.join(self.outgoing) + ']'
        return 'Node({0}, {1}, {2}, {3})'.format(self.name, self.kind, incoming, outgoing)

    def isKind(self, kind):
        return self.kind == kind

    def fol_come(self, time, edge_id, direction):
        return None
        
    def fol_stay(self, time, edge_id, direction):
        return None

class Connection(Node):
    """Simple node of the graph (-)."""
    def __init__(self, args):
        super(Connection, self).__init__(args[0], args[1], [args[2]], [args[3]])
    
    def fol_come(self, time, edge_id, direction):
        if not isinstance(direction, list):
            direction = [direction]
        prev_edge = self.incoming[0]
        return disjunction("t_{0}_{1}({2})".format(prev_edge, d, time) for d in direction)
    

class Notice(Connection):
    """Connection with signpost (|)."""
    def __init__(self, arg):
        super(Notice, self).__init__(arg)
        
    def fol_opened(self, time, edge_id, direction):
        return '{0}({1})'.format(self.name, time)
    
    def fol_come(self, time, edge_id, direction):
        if not isinstance(direction, list):
            direction = [direction]
        prev = self.incoming[0]
        conj = disjunction(["t_{0}_{1}({2})".format(prev, d, time) for d in direction])
        return "({0} & {1}{2})".format(conj, self.name, time)
    
    def fol_stay(self, time, edge_id, direction):
        if not isinstance(direction, list):
            direction = [direction]
        conj = disjunction(["t_{0}_{1}({2})".format(prev, d, time) for d in direction])
        return "({0} & ~{1}{2})".format(conj, self.name, time)

class Coupler(Node):
    """Coupler with signpost (>)"""
    def __init__(self, args):
        super(Coupler, self).__init__(args[0], args[1],args[2:4], [args[4]])
    
    def fol_come(self, time, edge_id, direction):
        if not isinstance(direction, list):
            direction = [direction]
        prev1 = self.incoming[0]
        prev2 = self.incoming[1]
        conj1 = disjunction(["t_{0}_{1}({2})".format(prev1, d, time) for d in direction])
        conj2 = disjunction(["t_{0}_{1}({2})".format(prev2, d, time) for d in direction])
        return "(({0} & {2}({3})) | ({1} & ~{2}({3})))".format(conj1, conj2, self.name, time)
    
    def fol_stay(self, time, edge_id, direction):
        if not isinstance(direction, list):
            direction = [direction]
        conj = disjunction(["t_{0}_{1}({2})".format(edge_id, d, time) for d in direction])
        if self.incoming.index(edge_id) == 0:
            return "({0} & ~{1}({2}))".format(conj, self.name, time)
        else:
            return "({0} & {1}({2}))".format(conj, self.name, time)

class Tournout(Node):
    """Tournout with signpost (<)"""
    def __init__(self, args):
        super(Tournout, self).__init__(args[0], args[1],[args[2]], args[3:5])
    
    def fol_opened(self, time, edge_id, direction):
        if self.outgoing.index(edge_id) == 0:
            return '{0}({1})'.format(self.name, time)
        else:
            return '~{0}({1})'.format(self.name, time)
    
    def fol_come(self, time, edge_id, direction):
        if not isinstance(direction, list):
            direction = [direction]
        prev = self.incoming[0]
        conj = disjunction(["t_{0}_{1}({2})".format(prev, d, time) for d in direction])
        if self.outgoing.index(edge_id) == 0:
            return "({0} & {1}({2}))".format(conj, self.name, time)
        else:
            return "({0} & ~{1}({2}))".format(conj, self.name, time)

class Input(Node):
    """Input with signpost (I)"""
    def __init__(self, args):
        super(Input, self).__init__(args[0], args[1], [], [args[2]])
    
    def fol_come(self, time, edge_id, direction):
        return "{0}({1})".format(self.name, time)


class Output(Node):
    """Output node (O)"""
    def __init__(self, args):
        super(Output, self).__init__(args[0], args[1], [args[2]], [])

def gen_edges(node):
    """Edge generator form nodes"""
    for id in node.incoming:
        yield Edge(id, None, node.name)
    for id in node.outgoing:
        yield Edge(id, node.name, None)
        
class Graph(object):
    """Rail graph"""
    def __init__(self):
        super(Graph, self).__init__()
        self.nodes = dict()
        self.edges = dict()
        self.inputs = []
        self.outputs = []
        self.reachability = None
        
    def add_node(self, node):
        """Add node to graph."""
        self.nodes[node.name] = node
        node.graph = self
        for edge in gen_edges(node):
            self.__add_edge(edge)
        if node.isKind(INPUT) and not node.name in self.inputs:
            self.inputs.append(node.name)
        if node.isKind(OUTPUT) and not node.name in self.outputs:
            self.outputs.append(node.name)
        
    def __add_edge(self, edge):
        if edge.name in self.edges:
            self.edges[edge.name].merge(edge)
        else:
            self.edges[edge.name] = edge

    def get_node(self, node_id):
        return self.nodes[node_id]
    
    def get_edge(self, edge_id):
        return self.edges[edge_id]

    def reversed_edges(self, node_id):
        """Generator of edger in reverse form given node."""
        
    def __expand_edge_reversed(self, edge):
        """Expand node by incoming edges."""
        node = self.get_node(edge.head_id)
        for edge_id in node.incoming:
            yield self.get_edge(edge_id)

    def edges_rbfs(self, node_id):
        """Reversed edges breath first search from given node."""
        node = self.get_node(node_id)
        open_list = []
        for edge_id in node.incoming:
            open_list.append(self.get_edge(edge_id))

        while len(open_list) > 0:
            edge = open_list.pop()
            for e in self.__expand_edge_reversed(edge):
                open_list.insert(0, e)
            yield edge
    
    def get_all_nodes(self, f=None):
        for node in self.nodes.values():
            if (not f) or node.isKind(f):
                yield node
    
    def reachable_outputs(self, edge_id):
        """Reachable outputs for give """
        if not self.reachability:
            self.__update_reachability()
        return self.reachability[edge_id]
    
    
    def __update_reachability(self):
        """Update reachability"""
        self.reachability = dict()
        for output in self.outputs:
            for edge in self.edges_rbfs(output):
                if not edge.name in self.reachability:
                    self.reachability[edge.name] = [output]
                else:
                    self.reachability[edge.name].append(output)
    
    def dump(self):
        print ">> Nodes:\n" + ', '.join(str(n) for n in self.nodes.values())
        print ">> Edges:\n" + ', '.join(str(e) for e in self.edges.values())
        print ">> Inputs: " + ', '.join(self.inputs)
        print ">> Outputs: " + ', '.join(self.outputs)
        if not self.reachability: self.__update_reachability()
        print ">> Reachability:\n" + ', '.join(str(i) for i in self.reachability.items())


element_parser = { 
  INPUT         : lambda p: Input(p),
  OUTPUT        : lambda p: Output(p), 
  CONNECTION    : lambda p: Connection(p),
  NOTICE        : lambda p: Notice(p),
  COUPLER       : lambda p: Coupler(p),
  TOURNOUT      : lambda p: Tournout(p)
}

def input_filter(stream):
    """Filte input file."""
    for line in stream:
        if line[-1] == '\n':
            line = line[:-1]
        index = line.find('#')
        if index >= 0:
            line = line[:index]
        line = line.strip()
        if len(line) > 0:
            yield line

def parse_node(line):
    """Parse one line of rail formated file: line => Node"""
    elm = line.split()
    return element_parser[elm[1]](elm)

def parse_graph(stream):
    """Parse whole file: file => Graph"""
    graph = Graph()
    for line in input_filter(stream):
        node = parse_node(line)
        graph.add_node(node)
    return graph


if __name__ == '__main__':
    import fileinput
    print "Node parsing:"
    for line in input_filter(fileinput.input()):
        node = parse_node(line)
        print node
    print "Graph parsing:"
    graph = parse_graph(fileinput.input())
    graph.dump()
    
    for out in graph.outputs:
        print "Traverse from " + out
        print ', '.join(str(e) for e in graph.edges_rbfs(out))
    
    
    for node in graph.get_all_nodes():
        for output in graph.outputs:
            for edge_id in node.incoming:
                print "node={4:s} seg={0} dir={1} fol:  {2} / {3}".format(
                    edge_id,
                    output,
                    node.fol_open('T', edge_id, output),
                    node.fol_closed('T', edge_id, output),
                    node
                    )

    
