## IOWeb Framework

Python framework to build web crawlers.

Good things:

 * system designed to run large number of network threads (like 100 or 500) on
    single CPU core
 * feature to combine things in chunks and then doing something with
    chunks (like mongodb bulk write)
 * asynchronous network operations are powered by gevent
 * network requests are handled with urllib3
 * HTML is parsed with lxml
 * ability to do CSS/XPATh queries to DOM tree of downloaded HTML document
 * ability to extract cert details
 * ability to resolve particular domain to custom IP
 * stat module to count events
 * logging statistics to influxdb
 * retrying on network errors

Bad things:

 * not fully covered with tests
 * no documentation

## Feedback

 * [t.me/grablab](https://t.me/grablab) - English chat about web scraping
 * [t.me/grablab_ru](https://t.me/grablab_ru) - Russian chat about web scraping
