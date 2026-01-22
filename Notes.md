# Build:
- Check containers/images: `docker ps --all`, `docker images`, `docker logs cicd_server_latest`
- Check file structure: `docker run -it --rm --entrypoint bash smcsde/cicd:server_latest`
- Clean: `docker image prune -a`, `docker container prune -a`

# Use:
- Client message send format: `<task> [<value>]` with
  - `l <file>`: Load ANN data from `file`
  - `s <file>`: Save ANN data to `file`
  - `i <point>`: Interpolate at `point`
  
# TODO:
- fix import error for `ann` in server
