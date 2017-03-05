import sys
import json
import networkx as nx
import Queue

def gn_algo(dataitem):
    G = nx.Graph()
    for item in dataitem:   #Adding nodes and edges to the graph G.
            G.add_nodes_from(item)
            G.add_edge(item[0],item[1])
    Nodes = G.nodes()
    Edges = G.edges()
    for everyedge in G.edges():
          sum_of_edge = 0
          Node0 = everyedge[0]
          Node1 = everyedge[1]
          G[Node0][Node1]['sum1'] = 0
    for root_node in Nodes:
         Discover = []
         DAG = nx.Graph()
         DAG_traversal = bfs_algo(G,DAG,root_node,Discover)
         rootList = []
         updateList = []
         top_dowm_step = top_down(DAG_traversal,root_node,G,DAG,rootList)
         bottom_up_step = bottom_up(DAG,DAG_traversal,root_node,Discover)

         for everyedge in G.edges(): #searching for every edge in the DAG Graph.
                Node0 = everyedge[0]
                Node1 = everyedge[1]
                if DAG.has_edge(Node0,Node1):
                    G[Node0][Node1]['sum1'] = G[Node0][Node1]['sum1'] + DAG[Node0][Node1]['weight']  #Adding all the values of the edge weight of every DAG.

    for everyedge in G.edges():
                Node0 = everyedge[0]
                Node1 = everyedge[1]
                Final_sum = float(G[Node0][Node1]['sum1'])/2 #Dividing by 2 because it is undirected graph.
                nodelist = [Node0,Node1]
                sorted(nodelist)
                jenc = json.JSONEncoder()
                print jenc.encode(nodelist),":",Final_sum



def bfs_algo(G,DAG,root_node,Discover):
  # "*********************BFS ALGO**************************"
  Nodes = G.nodes()
  for nodes in G.nodes():
      DAG.add_node(nodes)
      DAG.node[nodes]['stage']=0  #stage is used to specify the level of the node in the BFS traversal
  queue = Queue.Queue()
  Discover.append(root_node)
  G.node[root_node]=0
  DAG.node[root_node]['stage']=0
  queue.put(root_node)
  while not queue.empty():
      sub_nodes = queue.get()
      neighbors = G.neighbors(sub_nodes)
      for element in neighbors:
          if G.node[sub_nodes]!= G.node[element]:
              DAG.add_edge(sub_nodes,element)
          if element not in Discover:
                  queue.put(element)
                  Discover.append(element)
                  G.node[element] = G.node[sub_nodes]+1
                  DAG.node[element]['stage'] = DAG.node[sub_nodes]['stage']+1
  return DAG.edges()


def top_down(DAG_traversal,root_node,G,DAG,rootList):
    updateList = []
    neighbor_nodes = sorted((DAG.neighbors(root_node)))
    for neighbor in DAG.nodes() :
      DAG.node[neighbor]['index']=0  #Adding Index attribute to count the no of shotest paths.
    updateList.append(root_node)
    DAG.node[root_node]['index']=1
    queue = Queue.Queue()
    queue.put(root_node)
    while not queue.empty():
        sub_nodes = queue.get()
        neighbors1 = DAG.neighbors(sub_nodes)
        for element in neighbors1:
            if DAG.node[element]['stage']>DAG.node[sub_nodes]['stage']:
                DAG.node[element]['index'] = DAG.node[element]['index']+ DAG.node[sub_nodes]['index']
            if element not in updateList:
                    queue.put(element)
                    updateList.append(element)


def bottom_up(DAG,DAG_traversal,root_node,Discover):
    revDiscover = []
    for rev in reversed(Discover):  #for botton up traveral we will consider reverse of the discover list
        revDiscover.append(rev)
    parent_child_dict = {}
    child_parent_dict = {}
    parentList = []
    leafnodeList = []
    for nodes in revDiscover:
        childList =[]
        parentList = []
        neighbor = DAG.neighbors(nodes)
        for neighbor_node in neighbor:
           if DAG.node[nodes]['stage']<DAG.node[neighbor_node]['stage']:
              childList.append(neighbor_node)
           parent_child_dict[nodes] = childList
           if DAG.node[nodes]['stage']>DAG.node[neighbor_node]['stage']:
               parentList.append(neighbor_node)
           child_parent_dict[nodes] = parentList
        DAG.node[nodes]['value'] = 1

    for leafnode, value in parent_child_dict.iteritems(): #having a separate list for leaf so that we can assign its F(X)=F'(X)
        if value == []:
            leafnodeList.append(leafnode)

    for vertice in revDiscover:
        formula_sum =0
        f_of_X = 1
        if vertice in leafnodeList:
            f_dash_of_X = f_of_X     #assigning leaf node vlaue = 1
        else:
            child = parent_child_dict[vertice]
            for subchild in child:
                f_dash_of_X= DAG.node[subchild]['value']
                parent_of_subchild = child_parent_dict[subchild]
                sum_of_deno=0
                for subparent in parent_of_subchild:
                    denominator = DAG.node[subparent]['index']   # specially calculating the denominator. Because it consider all parents of a node.
                    sum_of_deno = sum_of_deno+denominator
                formula_part1 = (float(DAG.node[vertice]['index'])/sum_of_deno)* f_dash_of_X   #calculating the half part of the node formula.
                formula_sum = formula_sum+ formula_part1
                formula_calculation = f_of_X + formula_sum   #adding F(X) for the node X to the half part of the formula
                f_dash_of_X =  DAG.node[subchild]['value']
                f_dash_of_X = DAG.node[subchild]['value']
                DAG.node[vertice]['value'] = formula_calculation  #updating the F'(X), so that it can use for its parent.
    # "****************************************Putting EDGE FORMULA******************************************************"
    for revnode in revDiscover:
        parent_of_child_List = child_parent_dict[revnode]
        if len(parent_of_child_List)>1:
            sum_of_index = 0
            for every_parent in parent_of_child_List:
                 sum_of_index = sum_of_index + DAG.node[every_parent]['index']
            # print sum_of_index,"index"
            for every_parent in parent_of_child_List:
                share = (float(DAG.node[every_parent]['index'])/sum_of_index)*DAG.node[revnode]['value']
                # print share,"-------------"
                DAG[every_parent][revnode]['weight'] = share
        if len(parent_of_child_List)==1:
            DAG[parent_of_child_List[0]][revnode]['weight'] = DAG.node[revnode]['value']






if __name__=="__main__":
    dataitem = []
    # formula_list = []
    with open(sys.argv[1]) as json_file: #Accessing the json data.
          for line in json_file:
              dataitem.append(json.loads(line))
          # print dataitem
    gn_algo(dataitem)
