
# ============================================================ Python.
import pprint
pp = pprint.PrettyPrinter(indent=2)
# ============================================================ External-Library.
import pandas as pd
# ============================================================ My-Library.
# ============================================================ Project.
from idebug import DataStructure as ds
# ============================================================ Global-Variables.



# ============================================================
# https://api.mongodb.com/python/current/api/pymongo/results.html#pymongo.results.UpdateResult
# ============================================================

def UpdateResult(clss, caller):
    print(f"{'*'*60}\n{caller}")
    print(f" acknowledged : {clss.acknowledged}")
    print(f" matched_count : {clss.matched_count}")
    print(f" modified_count : {clss.modified_count}")
    print(f" raw_result : {clss.raw_result}")
    print(f" upserted_id : {clss.upserted_id}")

def UpdateResults(obj, caller):
    print(f"{'*'*60}\n{caller}")
    docs = []
    for UpdateResult in obj.UpdateResults:
        doc = {
            'acknowledged':UpdateResult.acknowledged,
            'matched_count':UpdateResult.matched_count,
            'modified_count':UpdateResult.modified_count,
            'raw_result':UpdateResult.raw_result,
            'upserted_id':UpdateResult.upserted_id
        }
        docs.append(doc)
    df = pd.DataFrame(docs)
    ds.dframe(df)
    g = df.groupby('modified_count').count()
    ds.dframe(g)

# ============================================================
# https://api.mongodb.com/python/current/api/pymongo/results.html#pymongo.results.InsertManyResult
# ============================================================

def InsertManyResult(clss, caller):
    print(f"{'*'*60}\n{caller}")
    print(f" acknowledged : {clss.acknowledged}")
    print(f" inserted_ids : {clss.inserted_ids}")

def InsertOneResult(clss, caller):
    print(f"{'*'*60}\n{caller}")
    print(f" acknowledged : {clss.acknowledged}")
    print(f" inserted_id : {clss.inserted_id}")

def DeleteResult(clss, caller):
    print(f"{'*'*60}\n{caller}")
    print(f" acknowledged : {clss.acknowledged}")
    print(f" deleted_count : {clss.deleted_count}")
    print(f" raw_result : {clss.raw_result}")
