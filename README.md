# elasticstream
Lightweight script/library that streams JSON lines from Elasticsearch to stdout

# usage (script)
    usage: elasticstream [-h] [-u URL] [-i INDEX] [-d DSL] [-k KEEPALIVE]
                         [-s SIZE] [-t]
    
    optional arguments:
      -h, --help            show this help message and exit
      -u URL, --url URL     Elasticsearch REST endpoint URL (default: localhost:9200)
      -i INDEX, --index INDEX
                            Elasticsearch index to stream (wildcards allowed). (default: *)
      -d DSL, --dsl DSL     Elasticsearch DSL query or @file containing query. (default: {"query": {"match_all": {}}})
      -k KEEPALIVE, --keepalive KEEPALIVE
                            Duration to keep scroll alive. Tune according to --size. (default: 1m)
      -s SIZE, --size SIZE  Number of hits to scroll at once. Tune according to sharding. (default: 10)
      -t, --test            Test the query, print the total hits, and exit. (default: False)

# usage (library)
    from elasticstream import ElasticStream

    url = 'localhost:9200'
    index = '*'
    dsl = '{"query": {"match_all": {}}}'

    stream = ElasticStream(url, index, dsl, scroll_keepalive='1m', scroll_size='10')

    print 'Total hits: %d' % stream.total_hits

    for doc in stream:
        print doc
