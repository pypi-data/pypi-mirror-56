from elasticsearch import Elasticsearch
from config import Config


class ElasticSearchCluster:

    def connect_to_cluster(self):

        host = Config.HOST
        port = Config.PORT

        es = Elasticsearch(hosts = [
            {'host': host, 'port': port}
        ])

        print('Connected to elasticsearch cluster')
        return es



# connect_to_cluster()