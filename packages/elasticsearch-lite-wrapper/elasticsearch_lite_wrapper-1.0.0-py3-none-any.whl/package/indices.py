from es import ElasticSearchCluster
from Analyzer import CustomAnalyzer


instance = ElasticSearchCluster()
conn = instance.connect_to_cluster()
i = conn.indices
ca = CustomAnalyzer()


class Index:

    '''
        To analyze a piece of text with custom analyzer
        Custom analyzer can be configured in config.py
    '''

    def analyze_text(self, text):
        a = ca.get_custom_analyzer()
        a['text'] = text
        # return a
        return i.analyze(body=a)


    '''
        Open a closed index to make it available for search.
    '''
    def open_index(self, index):
        i.open(index = index)
        print('Index now open!')


    '''
        Close an index and remove its overhead from the cluster
    '''
    def close_index(self, index):
        i.close(index = index)
        print('Index closed!')
    

    '''
        Create an index in elasticsearch
    '''
    def create_index(self, index, config = {}):
        i.create(index = index, body = config)
        print('Index ' + index + ' created!')
    
    
    '''
        Delete an index in elasticsearch
    '''
    def delete_index(self, index):
        i.delete(index = index)
        print('Index ' + index + ' deleted successfully!')
    

    '''
        To check whether an index exists or not
    '''
    def index_exists(self, index):
        return i.exists(index = index)
    

    '''
        Returns information about a particular index
    ''' 
    def index_info(self, index):
        return i.get(index = index)
    

    '''
        Retrieve mapping definition of index or index/type.
    '''
    def index_mapping(self, index):
        return i.get_mapping(index = index)
    

    '''
        Retrieve mapping definition of a specific field.
    '''
    def field_mapping(self, index, fields):
        return i.get_field_mapping(index = index, fields = fields)


    '''
        Retrieve settings for one or more (or all) indices.
    '''
    def index_settings(self, index, name = ''):
        return i.get_settings(index = index, name = name)
