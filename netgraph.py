
class NetGraph(object):
    @staticmethod
    def SingleSPF(graph_dict, src_node): 
        SPF_INFINITY = 16000000
        distance_dict = dict()
        previous_node = dict()
        unvisited_set = set()
        nodes = graph_dict.keys()
        for node in nodes:
            if node == src_node:
                distance_dict[node] = 0
            else:
                distance_dict[node] = SPF_INFINITY
            previous_node[node] = None
            unvisited_set.add(node)

        while unvisited_set:
            minimal_distance = SPF_INFINITY
            closest_node = None
            for node in nodes:
                if node in unvisited_set:
                    if distance_dict[node] <= minimal_distance:
                        minimal_distance = distance_dict[node]
                        closest_node = node
            
            unvisited_set.remove(closest_node)
            if distance_dict[closest_node] == SPF_INFINITY:
                print(closest_node)
                break

            for neighbor in graph_dict[closest_node].keys():
                if neighbor in unvisited_set:
                    path_len = distance_dict[closest_node] + int(graph_dict[closest_node][neighbor])
                    if path_len < distance_dict[neighbor]:
                        distance_dict[neighbor] = path_len
                        previous_node[neighbor] = closest_node
        return distance_dict, previous_node

    @staticmethod
    def SingleSPF_ECMP(graph_dict, src_node): 
        SPF_INFINITY = 16000000
        ecmp_cntr = 1
        distance_dict = dict()
        previous_node = dict()
        unvisited_set = set()
        nodes = graph_dict.keys()
        for node in nodes:
            if node == src_node:
                distance_dict[node] = 0
            else:
                distance_dict[node] = SPF_INFINITY
            previous_node[node] = None
            unvisited_set.add(node)
        
        while unvisited_set:
            minimal_distance = SPF_INFINITY
            closest_node = None
            for node in nodes:
                if node in unvisited_set:
                    if distance_dict[node] <= minimal_distance:
                        minimal_distance = distance_dict[node]
                        closest_node = node
            
            unvisited_set.remove(closest_node)
            if distance_dict[closest_node] == SPF_INFINITY:
                break

            for neighbor in graph_dict[closest_node].keys():
                if neighbor in unvisited_set:
                    path_len = distance_dict[closest_node] + int(graph_dict[closest_node][neighbor])
                    if path_len <= distance_dict[neighbor]:
                        distance_dict[neighbor] = path_len
                        if previous_node[neighbor]:
                            previous_node[neighbor+"-e"+str(ecmp_cntr)] = closest_node
                            ecmp_cntr += 1
                        else:
                            previous_node[neighbor] = closest_node
        return distance_dict, previous_node

    @staticmethod
    def SrcDst_SPF_ECMP(graph_dict, src_node, dst_node): 
        #not realy ecmp (yet) :)
        SPF_INFINITY = 16000000
        ecmp_cntr = 1
        distance_dict = dict()
        previous_node = dict()
        unvisited_set = set()
        nodes = graph_dict.keys()
        for node in nodes:
            if node == src_node:
                distance_dict[node] = 0
            else:
                distance_dict[node] = SPF_INFINITY
            previous_node[node] = None
            unvisited_set.add(node)
        
        while unvisited_set:
            minimal_distance = SPF_INFINITY
            closest_node = None
            for node in nodes:
                if node in unvisited_set:
                    if distance_dict[node] <= minimal_distance:
                        minimal_distance = distance_dict[node]
                        closest_node = node
            
            unvisited_set.remove(closest_node)
            if closest_node == dst_node:
                break
            if distance_dict[closest_node] == SPF_INFINITY:
                break

            for neighbor in graph_dict[closest_node].keys():
                if neighbor in unvisited_set:
                    path_len = distance_dict[closest_node] + int(graph_dict[closest_node][neighbor])
                    if path_len < distance_dict[neighbor]:
                        distance_dict[neighbor] = path_len
                        if previous_node[neighbor]:
                            previous_node[neighbor+'-ecmp'+str(ecmp_cntr)] = previous_node[neighbor]
                            previous_node[neighbor] = closest_node
                            ecmp_cntr += 1
                        else:
                            previous_node[neighbor] = closest_node
        path_cntr = 1
        srcdst_path = dict()
        path_node = dst_node
        while previous_node[path_node]:
            srcdst_path[path_cntr] = path_node
            path_node = previous_node[path_node]
            path_cntr += 1
        pn1 = dict()
        for key in previous_node.keys():
            if previous_node[key] != None:
                pn1[key] = previous_node[key]
                
        return distance_dict[dst_node], srcdst_path


