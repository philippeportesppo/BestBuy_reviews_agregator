# BestBuy_reviews_agregator
Parse the BestBuy products under a provided Category Path and extract the reviews text and 5star ranking

An OS environment variable API_KEY_BBY must be defined with your BestBuy Developer API Key. Go to https://developer.bestbuy.com/ to register and get the key.

Example of usage: BestBuy_Reviews.py abcat0502000 

The scripts require a Category Path (here I put abcat0502000) value that every products below will be parsed. 

To identify this value, you can query a product of that category and check the response. 
Example: 
   curl "https://api.bestbuy.com/v1/categories(name=Sony%20DSLR%20Camera*)?format
Answer:
{
  "from": 1,
  "to": 1,
  "total": 1,
  "currentPage": 1,
  "totalPages": 1,
  "queryTime": "0.011",
  "totalTime": "0.014",
  "partial": false,
  "canonicalUrl": "/v1/categories(name=\"Sony DSLR Camera*\")?show=path&format=json&apiKey=YourAPIKey",
  "categories": [
    {
      "path": [
        {
          "id": "cat00000",
          "name": "Best Buy"
        },
        {
          "id": "pcmcat128500050004",
          "name": "Name Brands"
        },
        {
          "id": "cat15063",
          "name": "Sony"
        },
        {
        
          "id": "pcmcat97200050015",
          "name": "Sony DSLR Camera"
        }
      ]
    }
  ]
}

An optional export_SKU parameter allows to dump the SKU id related to the review.

Example: BestBuy_Reviews.py abcat0502000 export_SKU
