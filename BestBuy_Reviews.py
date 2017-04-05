import json
import requests
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import exceptions

import csv
import sys
import os

try:
    API_KEY = os.environ['API_KEY_BBY'] 
except:
    print "No API_KEY_BBY found in OS environment variables. Please define your Best Buy API key as an environment variable."
    exit()
print "Detected API_KEY_BBY: ",API_KEY

try:
    categorypath=sys.argv[1]
except:
    print "No product category path provided. (example: abcat0502000)"
    exit()
    
print "Detected category path: ",categorypath

export_SKU=False
try: 
    if sys.argv[2]=="export_SKU":
        export_SKU=True
except:
    print "No export_SKU set: only export rating and reviews"

REQUEST_URL_BASE = "https://api.bestbuy.com/v1/products(categoryPath.id="+categorypath+")?apiKey={API_KEY}&format=json&sort=sku.asc&show=sku&pageSize=100&page={page}"

sess = requests.Session()
sess.mount('https://', HTTPAdapter(max_retries=Retry(total=5, status_forcelist=[500,503,429])))

v = sess.get(REQUEST_URL_BASE.format(API_KEY=API_KEY, page="1"))
product = v.json()

totalPages=product['totalPages']
with open('Listbestbuy.tsv', mode='w') as fd:
    writer = csv.writer(fd, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_NONNUMERIC)
    for page_product in range (1, totalPages+1):
        try:
            q = sess.get(REQUEST_URL_BASE.format(API_KEY=API_KEY,page=str(page_product)))
            product = q.json()
            print product['canonicalUrl']
            print "========================"
            print "Page ",str(page_product)+"/"+str(totalPages)
            counterSKU=0
            counter = 0
            for sku_in_prod in product["products"]:
                SKU = sku_in_prod["sku"] 
                counterSKU+=1
                print "Sku: ",SKU," (", counterSKU,"/",len(product["products"]),")"
                
                REQUEST_URL = "https://api.bestbuy.com/v1/reviews(sku={sku})?apiKey={API_KEY}&show=comment,title,id,rating,reviewer.name,sku,submissionTime&pageSize=100&page={page}&sort=comment.asc&format=json"
                r = sess.get(REQUEST_URL.format(sku=str(SKU), API_KEY=API_KEY, page=1))
                
                try:
                    user_comments= r.json()
                    if user_comments['totalPages']!=None:
                        totalComments=user_comments['totalPages']
                                                
                        for i in range(1,totalComments+1): 
                            try:
                                REQUEST_URL = "https://api.bestbuy.com/v1/reviews(sku={sku})?apiKey={API_KEY}&show=comment,title,id,rating,reviewer.name,sku,submissionTime&pageSize=100&page={page}&sort=comment.asc&format=json"
                                
                                s = sess.get(REQUEST_URL.format(sku=str(SKU), API_KEY=API_KEY, page=str(i)))
                                data = s.json()
                                k=0
                                for reviews in data["reviews"]:
                                    k=k+1
                                    print "Review ",str(k)+" of page="+str(i)+"/ totalpages= "+str(totalComments)
                                    review_text = "".join([text.encode("utf8") for text in reviews[u'comment']])
                                    counter=counter+1
                                    if export_SKU==True:
                                        writer.writerow([counter, SKU, int(reviews['rating']), ''.join(review_text.splitlines())])
                                    else:
                                        writer.writerow([counter, int(reviews['rating']), ''.join(review_text.splitlines())])
                            except:
                                print "Error on request: (s)"
                                print sys.exc_info()
                                exit()
                                   
                    else: #only one page 
                        k=0
                        for reviews in user_comments["reviews"]:
                            k=k+1
                            print "Review ",str(k)
                            review_text = "".join([text.encode("utf8") for text in reviews[u'comment']])
                            counter=counter+1
                            if export_SKU==True:
                                writer.writerow([counter, SKU, int(reviews['rating']), ''.join(review_text.splitlines())])
                            else:
                                writer.writerow([counter, int(reviews['rating']), ''.join(review_text.splitlines())])
                    
                except:
                    print "Error on request: (r)"
                    print sys.exc_info()
                    print "===================="
                    print r
                    print "===================="
                    exit()
                
        except:
            print "Error on request: (q)"
            print sys.exc_info()
            exit()
fd.close