# Scooter-Sharing-Aggregator

Web-service with RESTful API that allows user to aggregate information about scooters among different scooter sharing apps. It also allows to book and unbook preferred scooter.


## User-to-Aggregator API


**GET** `/scooters` 

Response
- 200 OK

<br/>Response body example
```json
{
  "_links": {
    "self": { "href": "/scooters" },
    "new_client": { "href": "/scooters/new_client" },
    "nearest": { "href": "/scooters/nearest" }
  }
}
```

**GET** `/scooters/new_client`
</br>Get client id.

Response
- 200 - OK

<br/>Response body example
```json
{
   "client_id": 100200300,
  "_links": {
    "self": { "href": "/scooters" },
    "new_client": { "href": "/scooters/new_client" },
    "nearest": { "href": "/scooters/nearest" }
  }
}
```

**GET** `/scooters/nearest`
</br>Get nearest scooters.

Params:
- `lon`, `lat` - user coordinates
- `max_price`[optional] - max possible price for scooter driving per hour
- `limit`[optional] - max possible amount of nearest scooters in response

Response
- 200 - OK

<br/>Response body example
```json
{
  "scooters": [
    {
      "scooter_id": 1,
      "lon": 1,
      "lat": 0,
      "price": "1$/hour"
    }
  ],
  "_links": {
    "self": { "href": "/scooters/nearest" },
    "book": { "href": "/scooters/book" },
    "unbook": { "href": "/scooters/unbook" }
  }
}
```

**PUT** `/scooters/book`
</br>Ask to book the scooter in the 3d party app.

Params
- `uuid` - client id
- `scooter_id`

Response
- 204 - No Content - Success.
- 409 - Conflict - If the scooter already locked.

<br/>Response body example
```json
{  "message": "This scooter has already been locked." }
```

**PUT** `/scooters/unbook`
</br>Ask to unbook the scooter in the 3d party app.

Params
- `uuid` - client id
- `scooter_id`

Response
- 204 - No Content - Success.

### Supported HTTP Status Codes:
<br/>**200 OK** Successful request.
<br/>**204 No Content** The server has fulfilled the request but does not need to return an entity-body.
<br/>**400 Bad Request** Wrong URI or JSON representation of data.
<br/>**404 Not found** The requested resource could not be found.
<br/>**409 Conflict** Same or very similar resource already exists.
<br/>**500 Internal Server Error** Unexpected condition was encountered on server and request can't be handled.


## Aggregator-Scooter-Service API


**GET** `/vehicles`
</br>Gets all available scootres in the app.

Response
- 200 - OK

<br/>Response body example
```json
{
  "vehicles": [
    {
      "scooter_id": 1009,
      "lon": 10,
      "lat": 120,
      "price": "1$/hour"
    },
    {
      "scooter_id": 1008,
      "lon": 200,
      "lat": 500,
      "price": "1$/hour"
    }
  ]
}
```
**PUT** `/vehicles/book`

Parameters
- scooter_id
- uuid - client id

**PUT** `/vehicles/unbook`

Parameters
- scooter_id
- uuid - client id
