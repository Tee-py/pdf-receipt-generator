# Receipt PDF Generator Service With DjangoRestFramwork & WeasyPrint

This is An Online API for Generating Receipts PDF for Payments.

There is a swagger UI to interact with the API at [Dukka-API](https://dukka-app.herokuapp.com/api/docs/) API.


# API Documentation

![Sample Receipt](/recpt.png)

## Authorization

The API uses JWT Bearer Token For Authenticating Users.

To authenticate an API request, you should provide your JWT Token in the `Authorization` header. For example

```
{"Authorization": "Bearer <jwt access token>"}
```
`access` token expires every `120` minutes and `refresh` token expires every `2 days`.

## API Response

The API response is in the following format:
```javascript
{
  "status": bool,
  "message": string,
  "error_code": integer,
  "data": json object | dictionary
}
```
- The `success` attribute describes if the api call was successfull or not.
- The `message` attribute contains a message commonly used to indicate errors or, in the case of deleting a resource, success that the resource - was properly deleted.
- The `error_code` attribute indicates the type of error if any and it is `null` for a successfull request. `100` represents `validation errors` and `200` represents server errors.
- The `data` attribute contains any other metadata associated with the response. This will be an escaped string containing JSON data or `null`.

## Status Codes

Gophish returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |

## Create User

```http
POST /api/create_user/
```

### Authorization: No Auth

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `api_key` | `string` | **Required**. Your Gophish API key |
### Request Body

```javascript
{
  "email" : string,
  "password" : string
}
```

## Login

```http
POST /api/login/
```

### Authorization: No Auth

### Request Body

```javascript
{
  "email" : string,
  "password" : string
}
```

### Response

{
  "refresh": "string",
  "access": "string"
}

## Refresh Token

```http
POST /api/token/refresh/
```

### Authorization: No Auth

### Request Body

```javascript
{
  "refresh" : string
}
```

### Response

{
  "access": "string"
}

## Generate Receipt

```http
POST /api/receipt/
```

### Authorization: Bearer `JWT TOKEN`

### Request Body

```javascript
{
  "company_name": "Dukka Inc",
  "company_address": "8 Olusegun Aina St, Ikoyi 106104, Lagos, Nigeria.",
  "customer_name": "Oluwatobi Emmanuel",
  "customer_email": "tobiloba@gmail.com",
  "customer_address": "No 20, Ogunlana Drive, Surulere, Lagos, Nigeria.",
  "customer_mobile": "09034678789",
  "items": [
    {
      "description": "Samsung Buds Live Gold",
      "quantity": 1,
      "unit_price": "70000"
    },
    {
      "description": "Samsung S21 Ultra Black",
      "quantity": 1,
      "unit_price": "550000"
    }
  ]
}
```

### Response
```Javascript
{
  "status": true,
  "error_code": null,
  "message": "Receipt Generated Successfully",
  "data": null
}
```

## Fetch Receipts

```http
GET /api/receipt/
```

### Authorization: Bearer `JWT TOKEN`

### Response


### Response
```Javascript
{
  "status": true,
  "error_code": null,
  "message": "success",
  "data": [
    {
      "rid": "5F680B12228",
      "file": "https://res.cloudinary.com/teepy/image/upload/v1/media/receipts/recpt-5F680B12228.pdf",
      "data": {
        "company_name": "string",
        "company_address": "string",
        "customer_name": "string",
        "customer_email": "user@example.com",
        "customer_address": "string",
        "customer_mobile": "string",
        "items": [
          {
            "description": "string",
            "quantity": 1,
            "unit_price": "500"
          }
        ]
      }
    }
  ]
}
```

