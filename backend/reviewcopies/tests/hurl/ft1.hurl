POST http://localhost:8000/api/v1/auth/login/
{
  "username": "h000123",
  "password": "motdepasse"
}
HTTP 200
[Asserts]
jsonpath  "$.token" exists
[Captures]
token: jsonpath "$.token"

GET http://localhost:8000/api/v1/sessions/
Authorization: Bearer {{token}}
HTTP 200
[Asserts]
jsonpath "$" count == 1
jsonpath "$[0].slug" == "session-de-janvier-2025"

GET http://localhost:8000/api/v1/branches/session-de-janvier-2025/
Authorization: Bearer {{token}}
HTTP 200
[Asserts]
jsonpath "$" count == 2
jsonpath "$[*].slug" includes "bachelier-en-informatique-orientation-developpement-dapplications"
jsonpath "$[*].slug" includes "bachelier-en-comptabilite"

GET http://localhost:8000/api/v1/schedules/session-de-janvier-2025/bachelier-en-informatique-orientation-developpement-dapplications/
HTTP 200
[Asserts]
jsonpath "$" count == 3
