import pandas as pd
import json
import ijson
import graphlab
import ast
from scipy.spatial.distance import cosine
import numpy as np
import scipy.stats
import scipy.spatial
from sklearn.cross_validation import KFold
import random
from sklearn.metrics import mean_squared_error
from math import sqrt
import math
import warnings
import sys

graphlab.product_key.set_product_key("CC89-D076-1805-CAA3-166E-BF94-5FC1-1688")


business = []
with open('buisness.json') as f:
    for line in f:
        business.append(json.loads(line))

business2 = []
b_cols = ['business_id', 'name', 'longitude', 'latitude']

for b in business:
	dummy = {}
	for column_name in b_cols :
		dummy[column_name] = b[column_name]
	business2.append(dummy)

businessDF = pd.DataFrame(business2)


reviews = []
with open('reviews_business.txt') as f:
    for line in f:
		json_data = ast.literal_eval(line)
		json_data = json.dumps(json_data)
		reviews.append(json.loads(json_data))


reviews2 = []
b_cols = ['business_id', 'user_id', 'stars']
for b in reviews:
	dummy = {}
	for column_name in b_cols :
		dummy[column_name] = b[column_name]
	reviews2.append(dummy)

reviewsDF = pd.DataFrame(reviews2)

# usernames = []
# users = []
# for rev in reviews2:
# 	if rev['user_id'] in usernames :
# 		users[usernames.index(rev['user_id'])]['count'] += 1
# 		users[usernames.index(rev['user_id'])]['stars'] += rev['stars']
# 	else :
# 		user = {}
# 		user['id'] = rev['user_id']
# 		user['count'] = 1
# 		user['stars'] = rev['stars']
# 		users.append(user)
# 		usernames.append(rev['user_id'])

# itemnames = []
# items = []
# for rev in reviews2:
# 	if rev['business_id'] in itemnames :
# 		items[itemnames.index(rev['business_id'])]['count'] += 1
# 		items[itemnames.index(rev['business_id'])]['stars'] += rev['stars']
# 	else :
# 		item = {}
# 		item['id'] = rev['business_id']
# 		item['count'] = 1
# 		item['stars'] = rev['stars']
# 		items.append(item)
# 		itemnames.append(rev['business_id'])

# # print len(usernames)
# # print len(itemnames)

# combnames = []
# combs = []
# for rev in reviews2:
# 		item = {}
# 		item['business_id'] = rev['business_id']
# 		item['user_id'] = rev['user_id']
# 		combnames.append(item)


# for uname in usernames :
# 	for iname in itemnames :
# 		if {'user_id' : uname, 'business_id' : iname} not in combnames:
# 			reviews2.append({'user_id' : uname, 'business_id' : iname, 'stars' : 0})
# 			combnames.append({'user_id' : uname, 'business_id' : iname})


# length = len(usernames)
# print length
# print len(itemnames)

# w, h = length, length;
# sim = [[0 for x in range(w)] for y in range(h)] 


# for idx1, firstuser in enumerate(usernames) :
# 	for idx2, seconduser in enumerate(usernames) :
# 		if firstuser != seconduser :
# 			similarity = 0.0
# 			for item in itemnames :
# 				comb1 = combnames.index({'user_id' : firstuser, 'business_id' : item})
# 				comb2 = combnames.index({'user_id' : seconduser, 'business_id' : item})
# 				similarity = similarity + (reviews2[comb1]['stars']*reviews2[comb2]['stars'])/(users[usernames.index(firstuser)]['stars']*items[itemnames.index(item)]['stars']*1.0)
# 				# print reviews2[comb1]['stars'] , reviews2[comb2]['stars'], users[usernames.index(firstuser)]['stars'], items[itemnames.index(item)]['stars'], (reviews2[comb1]['stars']*reviews2[comb2]['stars'])/(users[usernames.index(firstuser)]['stars']*items[itemnames.index(item)]['stars']*1.0), similarity
# 			sim[idx1][idx2] = similarity
			
# for rev in reviews2 :
# 	if rev['stars'] == 0 :
# 		star = users[usernames.index(rev['user_id'])]['stars']/(users[usernames.index(rev['user_id'])]['count']*1.0)
# 		for user in usernames :
# 			if user != rev['user_id'] and reviews2[combnames.index({'user_id' : user, 'business_id' : rev['business_id']})]['stars'] != 0 :
# 				star += sim[usernames.index(rev['user_id'])][usernames.index(user)]*(reviews2[combnames.index({'user_id' : user, 'business_id' : rev['business_id']})]['stars'] - users[usernames.index(user)]['stars']/(users[usernames.index(user)]['count']*1.0))
# 		reviews2[combnames.index({'user_id' : user, 'business_id' : rev['business_id']})]['stars'] = star

# with open('data.txt', 'w') as outfile:
#     json.dump(reviews2, outfile)










# test = []
# with open('test.json') as f:
#     for line in f:
#         test.append(json.loads(line))

# test2 = []
# b_cols = ['business_id', 'user_id', 'stars']
# for b in test:
# 	dummy = {}
# 	for column_name in b_cols :
# 		dummy[column_name] = b[column_name]
# 	test2.append(dummy)

# testDF = pd.DataFrame(test2)
data = graphlab.SFrame(reviewsDF)
train, test = graphlab.recommender.util.random_split_by_user(data, user_id='user_id',item_id='business_id')

# popularity_model = graphlab.popularity_recommender.create(train, user_id='user_id', item_id='business_id', target='stars')
# popularity_recomm = popularity_model.recommend(k=2)
# popularity_recomm.print_rows(num_rows=25)

item_sim_model = graphlab.item_similarity_recommender.create(train, user_id='user_id', item_id='business_id', target='stars', similarity_type='cosine')
# item_sim_model.evaluate(test,target='stars')
item_sim_model.save('item_sim_model')
# graphlab.item_similarity_recommender.evaluate(item_sim_model,target='stars')
# item_sim_recomm = item_sim_model.recommend(k=5)
# item_sim_recomm.print_rows(num_rows=25)

fact_reco_model = graphlab.recommender.factorization_recommender.create(train,user_id='user_id', item_id='business_id', target='stars')
# fact_reco_model.evaluate(test,target='stars')
fact_reco_model.save('fact_reco_model')
# fact_reco_recomm = fact_reco_model.recommend(k=5)
# fact_reco_recomm.print_rows(num_rows=25)


fact_reco_model2 = graphlab.recommender.ranking_factorization_recommender.create(train,user_id='user_id', item_id='business_id', target='stars')
# fact_reco_model2.evaluate(test,target='stars')
fact_reco_model2.save('fact_reco_model2')
# fact_reco_recomm2 = fact_reco_model2.recommend(k=5)
# fact_reco_recomm2.print_rows(num_rows=25)

# model_performance = graphlab.compare(test, [popularity_model, item_sim_model, fact_reco_model, fact_reco_model2], metrics)
# graphlab.show_comparison(model_performance,[popularity_model, item_sim_model])


# print reviewsDF.groupby(by='business_id')['stars'].mean().sort_values(ascending=False).head(100)



# users = []
# for rev in reviewsDF:
# 	user = {}
# 	user['id'] = rev['user_id']

	# users[rev['user_id']] = {}
	# users[rev['user_id']]['count'] += 1;
	# users[rev['user_id']]['rev'] += rev['stars'];

# print users[0:5]