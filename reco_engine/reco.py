import pandas as pd
import json
import graphlab
import ast
from geopy.distance import vincenty
from geopy.distance import great_circle
from math import radians

graphlab.product_key.set_product_key("CC89-D076-1805-CAA3-166E-BF94-5FC1-1688")

business = []
with open('./reco_engine/business3.json') as f:
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

# item_sim_model = graphlab.load_model('./reco_engine/item_sim_model')
fact_reco_model = graphlab.load_model('./reco_engine/fact_reco_model')
# fact_reco_model2 = graphlab.load_model('./reco_engine/fact_reco_model2')

def find_dist(lat, lon, business_id):
	business = businessDF['business_id'] == business_id
	busi = businessDF[business]
	lat1 =  busi['latitude'].iloc[0]
	lon1 = busi['longitude'].iloc[0]
	# lat = radians(lat)
	# lon = radians(lon)
	# lat1 = radians(lat1)
	# lon1 = radians(lon1)
	point1 = (lat, lon)
	point2 = (lat1, lon1)
	# print point1, point2
	return great_circle(point1, point2).meters

def give_reco(user,lat,lon):
	items = []
	result = []
	# for item in business2 :
	# 	if find_dist(lat,lon,item['business_id']) <= 1000 :
	# 		items.append(item['business_id'])
	fact_reco_recomm = fact_reco_model.recommend(users = [user],items=items,k=200)
	cnt = 0
	for reco in fact_reco_recomm :
		if find_dist(lat,lon,reco['business_id']) <= 1000 :
			item = {}
			business = businessDF['business_id'] == reco['business_id']
			busi = businessDF[business]
			item['lat'] = busi['latitude'].iloc[0]
			item['lon'] = busi['longitude'].iloc[0]
			item['name'] = busi['name'].iloc[0]
			result.append(item)
			cnt += 1
			if cnt >= 5 :
				break

	if cnt < 3 :
		fact_reco_recomm = fact_reco_model.recommend(users = [user],items=items,k=1000)
		cnt = 0
		result = []
		for reco in fact_reco_recomm :
			if find_dist(lat,lon,reco['business_id']) <= 1000 :
				item = {}
				business = businessDF['business_id'] == reco['business_id']
				busi = businessDF[business]
				item['lat'] = busi['latitude'].iloc[0]
				item['lon'] = busi['longitude'].iloc[0]
				item['name'] = busi['name'].iloc[0]
				result.append(item)
				cnt += 1
				if cnt >= 5 :
					break

	return {"items" : result}



# print give_reco('V_4GSrSg7AK_5wXs9TrBbg',12.9354922,77.6146828,)
