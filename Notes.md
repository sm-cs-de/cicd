# Build:
- Check containers/images: `docker ps --all`, `docker images`, `docker logs cicd_server_latest`
- Check file structure: `docker run -it --rm --entrypoint bash smcsde/cicd:server_latest`
- Clean: `docker image prune -a`, `docker container prune`

# Use:
- Client message send format: `<task> [<value>]` with
  - `c <dim>`: Create ANN to interpolate `dim` using (x,y)-points
  - `i <point>`: Interpolate at `point`
  - `l <file>`: Load ANN data from `file`
  - `s <file>`: Save ANN data to `file`
  - `t <num>`: Train ANN using `num` samples
