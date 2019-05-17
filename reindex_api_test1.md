DELETE _all

GET _cat/aliases?v
GET _cat/indices?v

POST _reindex
{
  "source": {
    "remote": {
      "host": "http://es2:9200"
    },
    "index": "records-record-v1.0.0"
  },
  "dest": {
    "index": "records-record-v1.0.0-new"
  },
  "script": {
    "lang": "painless",
    "source": "ctx._source.name = ctx._source.title"
  }
}

GET records-record-v1.0.0-new/_search