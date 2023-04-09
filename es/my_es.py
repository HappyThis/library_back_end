from elasticsearch import Elasticsearch


class elastic_search:

    def __init__(self, index_type: str, index_name: str, ip="127.0.0.1"):

        self.es = Elasticsearch("http://localhost:9200", http_auth=('elastic', 'xLI19t03Oqf8x*mExQdN'))
        self.index_type = index_type
        self.index_name = index_name

    def create_index(self):
        if self.es.indices.exists(index=self.index_name) is True:
            self.es.indices.delete(index=self.index_name)
        self.es.indices.create(index=self.index_name, ignore=400)

    def delete_index(self):
        try:
            self.es.indices.delete(index=self.index_name)
        except:
            pass

    def get_doc(self, uid):
        return self.es.get(index=self.index_name, id=uid)

    def count(self):
        return self.es.count(index=self.index_name)

    def insert_one(self, doc: dict):
        self.es.index(id=doc['id'], index=self.index_name, body=doc)

    def insert_array(self, docs: list):
        for doc in docs:
            self.es.index(id=doc['id'], index=self.index_name, body=doc)

    def update_array(self, docs: list):
        for doc in docs:
            self.es.update(index=self.index_name, id=doc['id'], body={
                "doc": {
                    "book_name": doc["book_name"], "author": doc["author"],
                    "author_introduction": doc["author_introduction"], "abstract": doc["abstract"],
                    "catalog": doc["catalog"], "isbn": doc["isbn"],
                    "translator": doc["translator"],
                    "publisher": doc["publisher"], "picture": doc["picture"]
                }
            })

    def del_array(self, doc_id: list):
        query = {
            "query": {
                "terms": {
                    "id": doc_id
                }
            }
        }
        self.es.delete_by_query(index=self.index_name, body=query)

    def search(self, query, count: int = 30):
        dsl = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"book_name": query}},
                        {"match": {"author": query}},
                        {"match": {"author_introduction": query}},
                        {"match": {"abstract": query}},
                        {"match": {"catalog": query}},
                        {"match": {"isbn": query}},
                        {"match": {"translator": query}}
                    ]
                }
            }
        }
        match_data = self.es.search(index=self.index_name, body=dsl, size=count)
        return match_data


es = elastic_search(index_type="book_data", index_name="book")
es.create_index()
