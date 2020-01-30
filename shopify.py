import requests
import random
import threading
import json
import time
from dhooks import Webhook, Embed

import datetime

webhook_url = ''#Your Webhook Url


#############################################################Config###########################################################
USER_AGENT =['Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
		'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
		'Mozilla/5.0 (iPhone; CPU iPhone O12_0 like Mac OX) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366',
		'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1',
		'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57',
		'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)',
		'Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
		'Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36',
		'Mozilla/5.0 (Linux; Android 8.0.0; SM-G930F Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36',
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
		'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
		'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
		]


def timeis():
	ts = time.time()

	time_is = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')  # Format Time

	return time_is

def post_discord(purl,title,price,image,available_sizes):
    hook = Webhook(webhook_url)
    embed = Embed(
        description='',
        color=0x5CDBF0,
        timestamp='now'
    )
    embed.set_author(name='Custom Shopify Monitor', icon_url='')
    embed.set_title(title=title, url=purl)
    embed.set_footer(text='@zyx898',icon_url='https://pbs.twimg.com/profile_images/1201960848073383937/XzQhFIiM_400x400.jpg') 
    embed.add_field(name='Link', value=purl, inline=True)
    embed.add_field(name='Stock', value=" | ".join(available_sizes), inline=False)
    embed.set_thumbnail(image)
    hook.send(embed=embed)


#############################################End of Config#############################################







#############################################Get Proxy#############################################





#############################################End of Get Proxy#############################################










#############################################Get Sku List#############################################




def get_skus():																														#return skus list
	


	#############################################New Skus#############################################


	new_skus = []

	skus_files = open('shopify_link.txt').readlines()																				#Open file and read

	for i in range(len(skus_files)):					

		sku = skus_files[i].strip("\n")																								#Read every line in the file

		new_skus.append(sku)																										#Add sku into skus list


	#############################################End of new Skus#############################################





	#############################################Old Skus List###############################################


	diction = eval(open('shopify_diction.txt').read()) 																			#load diction

	old_skus = [*diction]																											#Load all keys into diction


	#############################################end of old skus list#############################################






	#############################################Compare New and old List#########################################


	sku_difference = [c for c in new_skus if c not in old_skus]									

	if sku_difference:

		for i in range(len(sku_difference)):
		
			diction[str(sku_difference[i])] = ['New Product']																		#If is New product add to Diciton
		
		write_diction = open("shopify_diction.txt","w")																			# Open Diction and Write it down
		write_diction.write(str(diction))
		write_diction.close()

	return new_skus


#############################################End of Get Skus##############################################







#############################################Check Stock Task#############################################



def task(purl):

	available_sizes = []

	url = purl+'.js'


	headers = {

		'User-Agent': random.choice(USER_AGENT)
			}
	product_response = requests.request("GET", url, headers=headers,timeout=10)  

																																	#set timeout to 10 incase proxy die

	product_json = json.loads(product_response.text)																				# Load Response into json format

	product_sizes = product_json['variants']  													# product sizes

	for i in range(len(product_sizes)):

		if product_sizes[i]['available']  == True:    																				# if selectable that means it is in stock

			available_size = product_sizes[i]['title']				

			available_size = available_size.replace("\uff08"," ")

			available_size = available_size.replace("\uff09"," ")


			available_sizes.append(available_size)

	check_restock(product_json,available_sizes,purl)																					#Call Function to check for restock


####################################################END of Task###############################################################







#################################################Compare List#################################################################


def check_restock(product_json,available_sizes,purl):
		diction = eval(open('shopify_diction.txt').read()) 																			#Get Diction
		
		old_available_sizes = list(diction[purl])																						#Set it into a list eaier to Compare

		difference = [c for c in available_sizes if c not in old_available_sizes]  														#Comapre difference

		if difference:

			title = product_json['title']					 															#product title

			price = product_json['price'] 																	#product price

			image = 'https:'+product_json['images'][0] 															#product image


			post_discord(purl,title,price,image,available_sizes)

			print(diction)

			diction[purl] = available_sizes																							#Set old purl values into new values

			write_file = open("shopify_diction.txt","w+")

			print(diction)

			write_file.write(str(diction))																								#Write down the New Diction
			
			write_file.close()

			print(timeis() + "[ "+str(purl)+" ] --> Restocked..................................")
		else:
			print(timeis() + "[ "+str(purl)+" ] --> Monitoring..................................")





################################################################################################################################

def main():
	while True:

		skus = get_skus()																											#Get Skus List

		for i in range(len(skus)):					

			time.sleep(2)

			(threading.Thread(target=task, args=(skus[i],))).start()	



		time.sleep(2)		
		
main()
