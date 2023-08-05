from es import ElasticSearchCluster

instance = ElasticSearchCluster()
conn = instance.connect_to_cluster()


class Main:

    def bulk_query(self, index, body):
        return conn.bulk(index = index, body = body)
    
    def query_count(self, index, body):
        return conn.count(index = index, body = body, allow_no_indices = True, ignore_unavailable = True)

    def create_doc(self, index, body, id):
        return conn.create(index = index, body = body, id = id)

    def delete_doc(self, index, id):
        return conn.delete(index = index, id = id)

    def delete_doc_using_query(self, index, body, conflicts = 'abort'):
        return conn.delete_by_query(index = index, body = body, conflicts = conflicts)

    def doc_exists(self, index, id):
        return conn.exists(index = index, id = id)
    
    def get_doc(self, index, id):
        return conn.get(index = index, id = id)

    def get_doc_source(self, index, id):
        return conn.get_source(index = index, id = id)

    def search_query(self, body, index = ''):
        return conn.search(index = index, body = body)
    
    def update_doc(self, index, id, body):
        return conn.update(index = index, id = id, body = body)
    
    def update_doc_by_query(self, index, body):
        return conn.update_by_query(index = index, body = body)
    
    