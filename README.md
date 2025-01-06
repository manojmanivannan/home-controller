# Simple Home Automation Server



# Generate API

docker run --rm -v $(pwd):/local -u `id -u` openapitools/openapi-generator-cli:v7.7.0 generate -i /local/openapi.yaml -g python-fastapi -c /local/config.yaml -o /local/src/client

## TODO

- [x] Turn off a device
- [ ] Turn off all devices in a room
- [ ] Turn off all devices in the home