http://localhost:9091/ws_cierres/swagger-ui.html

http://localhost:9091/ws_cierres/swagger-ui/index.html


curl -X POST http://localhost:9091/ws_cierres/v1/claim-accounting/send \
  -H "Content-Type: application/json" \
  -d '{"product":"2012","comment":"2012_202602","user":"j36147"}'
