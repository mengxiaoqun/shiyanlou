#!/usr/bin/env python3
import sys
from pymongo import MongoClient

def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contents = db.contests

    pipeline =[
            {$match:{'user_id':user_id}},
            {$group:{
                '_id':'$user_id',
                'total_score':{$sum:'$score'},
                'total_time':{$sum:'$submit_time'}
                }}
             ]
    result = list(contents.aggregate(pipeline))
    if len(result) == 0:
        return 0,0,0
    
    data = result[0]
    
    
    pipeline = [
            {$group:{
                '_id':'$user_id',
                'total_score':{$sum:'$score'},
                'total_time':{$sum:'$submit_time'}
                }},
            {$match:{
                $or:[{'total_score':{$gt:data['total_score']},
                    {'total_score':data['total_score'],
                    'total_time':{$lt:data['total_time']}}
                    ]}
                }},
            {$group:{'_id':None,'count':{$sum:1}}}
            ]

    result = list(contents.aggregate(pipeline))
    if result:
        rank = result[0]['count']+1
    else:
        rank = 1
    return rank,data['total_score'],data['total_time']


if __name__ == '__main__':
    argvs = sys.argv
    if len(argvs) != 2:
        print('Parameter Error')
        sys.exit(1)
    user_id = int(sys.argv[1])
    get_rank(user_id)


    
