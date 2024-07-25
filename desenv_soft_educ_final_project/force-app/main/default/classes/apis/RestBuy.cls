@RestResource(urlMapping='/buy/*')
global with sharing class RestBuy {

    @HttpPost
    global static void handlePost() {
        RestRequest req = RestContext.request;
        RestResponse res = RestContext.response;
    
        try {
            String requestBody = req.requestBody.toString();

            BuyService.Purchase purchase = (BuyService.Purchase)JSON.deserialize(requestBody, BuyService.Purchase.class);
            BuyService.purchase(purchase);

            res.statusCode = 201;
            res.responseBody = Blob.valueOf('{"message": "Purchased!"}');
        } catch (Exception e) {
            res.statusCode = 500;
            res.responseBody = Blob.valueOf('{"error": "' + e.getMessage() + '"}');
        }
    }
}