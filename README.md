# elasticstream
Lightweight (no dependencies) Python script/library that streams from Elasticsearch documents to JSON lines or CSV
output

# bin/elasticstream usage
    usage: elasticstream [-h] [-u URL] [-i INDEX] [-k KEEPALIVE] [-s SIZE]
                         [-d DSL] [-f {jsonl,csv}] [-o OUTPUT]
    
    optional arguments:
      -h, --help            show this help message and exit
      -u URL, --url URL     Elasticsearch REST endpoint URL (default:
                            localhost:9200)
      -i INDEX, --index INDEX
                            Elasticsearch index to stream (wildcards allowed)
                            (default: *)
      -k KEEPALIVE, --keepalive KEEPALIVE
                            Duration to keep scroll alive. Tune according to
                            --size (default: 1m)
      -s SIZE, --size SIZE  Number of hits to scroll at once. Tune according to
                            sharding (default: 10)
      -d DSL, --dsl DSL     Elasticsearch DSL query or @file (e.g., "curl -d"
                            syntax) containing query (default: {"query":
                            {"match_all": {}}})
      -f {jsonl,csv}, --format {jsonl,csv}
                            Output format. JSON lines (jsonl) or CSV (csv)
                            (default: jsonl)
      -o OUTPUT, --output OUTPUT
                            Output file to stream to. If not stdout, prints
                            progress to stdout (default: <open file '<stdout>',
                            mode 'w' at 0x1082fd150>)

# elasticstream.ElasticStream usage
    from elasticstream import ElasticStream

    url = 'localhost:9200'
    index = '*'
    dsl = '{"query": {"match_all": {}}}'

    stream = ElasticStream(url, index, dsl, scroll_keepalive='1m', scroll_size='10')

    for hit in stream:
        print hit
