# API Authentication

The authentication endpoint is available at the /auth path and accepts POST requests.
When you want to authenticate a user, you need to send a JSON body that contains
both a username field and a password field. The API will validate these credentials
against the database and return a token if the authentication is successful.

For example, if you wanted to authenticate a user named "john" with password "secret123",
you would send a POST request to /auth with the following JSON body:

{
  "username": "john",
  "password": "secret123"
}

The server will then check if these credentials are valid. In other words, it will
query the database to see if there's a user with that username and if the password
matches. If everything checks out, meaning the credentials are correct, the API
will respond with a JSON object containing an access token that you can use for
subsequent authenticated requests.