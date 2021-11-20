# Scooter-Sharing-Aggregator

Web-service with RESTful API that allows user to aggregate information about scooters among different scooter sharing apps. It also allows to book and unbook preferred scooter.


## User-to-Aggregator API

**GET** `/api` 

Response
- 200 OK

<br/>Response body example
```json
{
  "_links": {
    "clients": { "href": "/clients" },
    "scooters": { "href": "/scooters" }
  }
}
```


**POST** `/clients`
</br>Register new client.

Response
- 201 - Created.

<br/>Response body example
```json
{
   "uuid": 100200300,
   "_links": {
     "self": { "href": "/clients" }
   }
}
```


**GET** `/scooters` 
</br>Gets all available scooters.

Response
- 200 OK

<br/>Response body example
```json
{
  "scooters": [
    {
      "scooter_id": 1,
      "lon": 1,
      "lat": 0,
      "price": 5
    }
  ],
  "_links": {
    "self": { "href": "/scooters" },
    "nearest": { "href": "/scooters/nearest" },
    "book": { "href": "/scooters/{id}/reservations" },
    "unbook": { "href": "/scooters/{id}/reservations" }
  }
}
```

**GET** `/scooters/nearest`
</br>Gets nearest available scooters.

Params:
- `lon`, `lat` - user coordinates
- `max_price`[optional] - max possible price for scooter driving per hour
- `limit`[optional] - max possible amount of the nearest scooters in response

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
      "price": 5
    }
  ],
  "_links": {
    "self": { "href": "/scooters/nearest" },
    "book": { "href": "/scooters/{id}/reservations" },
    "unbook": { "href": "/scooters/{id}/reservations" }
  }
}
```

**POST** `/scooters/{id}/reservations`
</br>Ask to book the scooter in the 3d party app.

Params
- `uuid` - client id

Response
- 204 - No Content - Success.
- 409 - Conflict - If the scooter has already been locked.

<br/>Response body example
```json
{  "message": "This scooter has already been locked." }
```

**DELETE** `/scooters/{id}/reservations`
</br>Ask to unbook the scooter in the 3d party app.

Params
- `uuid` - client id

Response
- 204 - No Content - Success.

### Supported HTTP Status Codes:
<br/>**200 OK** Successful request.
<br/>**201 Created**
<br/>**204 No Content** The server has fulfilled the request but does not need to return an entity-body.
<br/>**400 Bad Request** Wrong URI or JSON representation of data.
<br/>**404 Not found** The requested resource could not be found.
<br/>**409 Conflict** Same or very similar resource already exists.
<br/>**500 Internal Server Error** Unexpected condition was encountered on server and request can't be handled.


## Aggregator-Scooter-Service API


**GET** `/vehicles`
</br>Gets all available scooters in the app.

Response
- 200 - OK

<br/>Response body example
```json
{
  "vehicles": [
    {
      "scooter_id": 1009,
      "lon": 50,
      "lat": 40,
      "price": 1
    },
    {
      "scooter_id": 1008,
      "lon": 22,
      "lat": 12,
      "price": 1
    }
  ]
}
```
**POST** `/vehicles/{id}/reservations`

Parameters
- uuid - client id

**DELETE** `/vehicles/{id}/reservations`

Parameters
- uuid - client id
