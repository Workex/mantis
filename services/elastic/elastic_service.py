from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from utils.wxlogger import WxLogger


class ElasticService:
    """Elastic Service Class."""

    logger = None

    def __init__(self, client: Elasticsearch):
        if self.__class__.logger is None:
            ElasticService.logger = WxLogger(__name__).getLogger()
        self.client = client
        ElasticService.logger.info("client initiated")

    def create_index(self, name, delete=True):
        if self.client.indices.exists(name):
            if delete:
                self.client.indices.delete(name)
                ElasticService.logger.info("Index Deleted")
                self.client.indices.create(index=name)
                ElasticService.logger.info("Index Created")
            else:
                ElasticService.logger.info("Index Already Exist")
        else:
            self.client.indices.create(index=name)
            ElasticService.logger.info("Index Created")

    def create_mapping(self, index, mapping, delete=True):
        if self.client.indices.exists(index):
            if delete:
                self.client.indices.delete(index)
                ElasticService.logger.info("Index Deleted")
                self.client.indices.create(index=index, body=mapping)
                ElasticService.logger.info("Mapping Created")
            else:
                ElasticService.logger.info("Index Already Exists")
        else:
            self.client.indices.create(index=index, body=mapping)
            ElasticService.logger.info("Mapping Created")

    def search_data(self, index, query):
        res = None
        data = []
        try:
            res = self.client.search(index=index, body=query)
            for doc in res["hits"]["hits"]:
                source = doc["_source"]
                source["_id"] = doc["_id"]
                data.append(source)
            return data
        except Exception as ex:
            ElasticService.logger.error(f"{query} failed - Exception: {ex}")

    def search_by_id(self, index, id):
        try:
            res = self.client.get(index=index, id=id)
            source = res["_source"]
            source["_id"] = res["_id"]
            return source
        except Exception as ex:
            ElasticService.logger.error(f"search_by_id failed - Exception: {ex}")

    def create_doc(self, index, doc, refresh=False):
        """Create / Update a document in the index.

        :param index: index name
        :param doc: document
        :return: True/False based on sucess/failure
        """
        try:
            self.client.index(index=index, body=doc, refresh=refresh)
            ElasticService.logger.info("---doc_created---")
            return True
        except Exception as ex:
            ElasticService.logger.error(ex)
            return False

    def create_doc_by_id(self, index, id, doc, refresh=False):
        """Create / Update a document in the index.

        :param index: index name
        :param doc: document
        :return: True/False based on sucess/failure
        """
        try:

            resp = self.client.index(index=index, body=doc, id=id, refresh=refresh)
            ElasticService.logger.info("---doc_created---")
            return resp
        except Exception as ex:
            ElasticService.logger.error(ex)
            return False

    def update_doc(self, index, id, body, seq_no, primary_term, refresh=False):
        """Update the existing document.

        :param index: index name
        :type index: string
        :param id: document id
        :type id: string
        :param script: body object for update query
        :type script: object
        :return: True/False
        :rtype: bool
        """
        try:
            resp = self.client.update(
                index=index,
                id=id,
                body=body,
                refresh=refresh,
                if_primary_term=primary_term,
                if_seq_no=seq_no,
            )
            return resp
        except Exception as ex:
            ElasticService.logger.error(ex)
            return False

    def update_by_query(self, index, body):
        """updating the existing document by query."""
        try:
            self.client.update_by_query(
                index=index,
                body=body,
                conflicts="proceed",
                wait_for_completion=False,
            )
            return True
        except Exception as ex:
            ElasticService.logger.error(ex)
            return False

    def bulk_update(self, client, actions):
        """updating doc in bulk."""
        bulk(client=client, actions=actions)

    def build_bulk_create_body(self, index, data):
        """building bosy for bulk elastic doc creation."""
        elastic_bulk_query = []
        for item in data:
            id_ = str(item["_id"])
            del item["_id"]
            elastic_bulk_query.append(
                {
                    "_id": id_,
                    "_op_type": "index",
                    "_index": index,
                    "_source": item,
                },
            )
        return elastic_bulk_query

    def build_bulk_update_body(self, index, data):
        """building body for bulk update."""
        elastic_bulk_query = []
        for item in data:
            id_ = str(item["_id"])
            del item["_id"]
            elastic_bulk_query.append(
                {
                    "_id": id_,
                    "_op_type": "update",
                    "_index": index,
                    "doc": item,
                },
            )
        return elastic_bulk_query

    def get_doc_version(self, index, doc_id):
        try:
            res = self.client.get(index=index, id=doc_id)
            return {"seq_no": res["_seq_no"], "primary_term": res["_primary_term"]}
        except Exception as ex:
            ElasticService.logger.error(f" query failed - Exception: {ex}")
            return False

    def fetch_scroll(self, index, doc_type, query, scroll, id=False, others=None):
        """
        Fetch large ammount of data in a cursor manner where the data exceeds 10000 doc limit
        :param index: index_name
        :param doc_type: index_type
        :param query: query body
        :param scroll: scroll time
        :param id: response to return doc_id or not
        :return: array of documents from query result
        """
        data = []
        if doc_type is None:
            res = self.es.search(index=index, body=query, scroll=scroll)
        else:
            res = self.es.search(index=index, doc_type=doc_type, body=query, scroll=scroll)
        scroll_id = res["_scroll_id"]
        count = 0

        scrolling = True
        while scrolling:
            if res["hits"]["hits"]:
                for doc in res["hits"]["hits"]:
                    source = doc["_source"]
                    if id:
                        source["_id"] = doc["_id"]

                    if others is not None:
                        docs = doc[others["key"]]
                        i = 0

                        # for attaching the array elements to their respective keys
                        if others["type"] == "array":
                            while i < len(docs):
                                source[others["columns"][i]] = docs[i]
                                i += 1
                        # for attaching the object to the respective key
                        if others["type"] == "object":
                            if others["tree"] is not None:
                                for leaf in others["tree"]:
                                    docs = docs[leaf]
                                source[others["key"]] = docs
                    data.append(source)
                res = self.es.scroll(scroll_id=scroll_id, scroll=scroll)
                count += 1
                ElasticIndividualClient.logger.info("scroll request : {}".format(count))
            else:
                scrolling = False
        return data
