# BestBuy_reviews_agregator
Parse the BestBuy products under a provided Category Path and extract the reviews text and 5star ranking

2 Scripts are available:
BestBuy_Reviews only dump in a Listbestbuy.tsv file an id (counter), the 5 star ranking, the review text.
BestBuy_reviews_model_number dump in a Listbestbuy.tsv file an id (counter), the product SKU number, the 5 star ranking, the review text.

An OS environment variable API_KEY_BBY must be defined with your BestBuy Developer API Key. Go to https://developer.bestbuy.com/ to register and get the key.
The scripts require a Category Path value that every products below will be parsed. 

To identify this value, you can query a product of that category and check the response. 
Example: curl "https://api.bestbuy.com/v1/categories(name=Sony%20DSLR%20Camera*)?format
Answer:{
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
