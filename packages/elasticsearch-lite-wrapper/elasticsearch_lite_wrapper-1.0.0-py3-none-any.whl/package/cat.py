from es import ElasticSearchCluster


instance = ElasticSearchCluster()
conn = instance.connect_to_cluster()
i = conn.cat

class Cat:


    '''
        Provides a snapshot of how shards have located around the cluster and the state of disk usage.
    '''
    def cluster_state(self, node = ''):
        return i.allocation(node_id = node, format = 'json')
    

    '''
        Count provides quick access to the document count of the entire cluster, or individual indices.
    '''
    def doc_count(self, index = ''):
        return i.count(index = index, format = 'json')

    
    '''
        Cluster health description
    '''
    def cluster_health(self):
        return i.health(format = 'json')


    '''
        Provides a cross-section of each index
    '''
    def indices(self, index = ''):
        return i.indices(index = index)

    
    '''
        Cluster topology
    '''
    def node_topology(self):
        return i.nodes(format = 'json')

    
    '''
        Shard information
    '''
    def shards_info(self, index = ''):
        return i.shards(index = index, format = 'json')

    