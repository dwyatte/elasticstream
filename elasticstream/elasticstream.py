import json
import urllib2


class ElasticStream(object):
    """
    Class to handle Elasticsearch stream
    """

    def __init__(self, url, index, dsl, scroll_keepalive='1m', scroll_size='10'):
        """
        Initialize the context by performing the search once and storing context as fields such as the scroll_id,
        number of hits, and the mappings so that the keys are consistent across scrolls
        :param url: Elasticsearch host:port on which to execute query (e.g., localhost:9200)
        :param index: 'Elasticsearch index to query (*-wildcards allowed)'
        :param dsl: JSON string data specifying Elasticsearch DSL query
        :param scroll_keepalive: How long to keep the scroll context alive
        :param scroll_size: Size of scroll (multiplied by # shards)
        :return:
        """
        self.url = url if url.startswith('http://') else 'http://%s' % url
        self.index = index
        self.dsl = dsl
        self.scroll_keepalive = scroll_keepalive
        self.scroll_size = str(scroll_size)

        # the scroll id saves our context and will get updated with each scroll
        request = '%s/%s/_search?scroll=%s&size=%s&search_type=scan' % \
                  (self.url, self.index, self.scroll_keepalive, self.scroll_size)
        response = json.load(urllib2.urlopen(request, data=self.dsl))

        self.scroll_id = response['_scroll_id']
        self.hits = []
        self.hits_scrolled = 0
        self.hits_total = response['hits']['total']

    def _scroll(self):
        """
        Scroll through one self.scroll_size set of results and save the new scroll_id context, populating self.hits
        """
        request = '%s/_search/scroll?scroll=%s&scroll_id=%s' % (self.url, self.scroll_keepalive, self.scroll_id)
        response = json.load(urllib2.urlopen(request))

        self.scroll_id = response['_scroll_id']
        self.hits = [hit['_source'] for hit in response['hits']['hits']]

    def __iter__(self):
        """
        Make this class an iterator
        """
        return self

    def next(self):
        """
        Pop hits off self.hits
        """
        if self.hits_scrolled == self.hits_total:
            raise StopIteration
        if not self.hits:
            self._scroll()

        self.hits_scrolled += 1
        return self.hits.pop(0)
