from pymongo.errors import BulkWriteError


def bulk_write(db, item_type, ops, stat=None, retries=3):
    """
    Tries to apply `ops` Update operations to `item_type`
    collection with `bulk_write` method.
    Gives up if `retries` retries failed.

    Args:
        db - pymongo collection object
        item_type - name of collection
        ops - list of operations like UpdateOne
        stat - instance of `ioweb.stat:Stat`
        retries - number of retries
    """
    stat and stat.inc('bulk-write-%s' % item_type)
    for retry in range(retries):
        try:
            res = db[item_type].bulk_write(ops, ordered=False)
        except BulkWriteError as ex:
            if retry == (retries - 1):
                raise
            else:
                stat and stat.inc('bulk-write-%s-retry' % item_type)
        else:
            break
    return res
