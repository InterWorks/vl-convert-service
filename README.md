# VL-Convert Service - Self-Hosted

This project is a containerized, self-hosted version of the [Vega VL-Convert Service](https://github.com/vega/vl-convert-service). It migrates the original Vercel serverless functions to a Flask web application that can be deployed in Docker containers for better control, reliability, and integration with your own infrastructure.

## Features

- **Self-hosted**: Run on your own servers instead of relying on external services
- **Docker containerized**: Easy deployment and scaling
- **API compatible**: Maintains the same API endpoints as the original Vercel service
- **Optimized fonts**: Uses web-optimized WOFF fonts downloaded from CDN during build
- **Production ready**: Includes gunicorn WSGI server and proper security practices

The service provides a REST API to [VlConvert](https://github.com/vega/vl-convert) for converting Vega-Lite and Vega specifications to various formats.

# Endpoints
The following endpoints are available

## `vl_version` Query parameter
All the endpoints that accept a Vega-Lite specification support a query parameter named `vl_version`, which defines the version of the Vega-Lite library that should be used. See [VlConvert Release Notes](https://github.com/vega/vl-convert/releases/) for info on the supported versions. Defaults to the latest Vega-Lite version.

## GET `/api/version`
Retrieve the version of VlConvert that is backing the API

## POST `/api/vl2vg`
Compile a Vega-Lite spec to a Vega spec. The Vega-Lite spec should be provided as the request body. The following optional query parameters are supported:
 - `vl_version`: The Vega-Lite version.

## POST `/api/vl2svg`
Convert a Vega-Lite spec to an SVG image. The Vega-Lite spec should be provided as the request body. The following optional query parameters are supported:
 - `vl_version`: The Vega-Lite version.
 - `theme`: Named theme as supported by [vega-themes](https://github.com/vega/vega-themes).

## POST `/api/vl2png`
Convert a Vega-Lite spec to a PNG image. The Vega-Lite spec should be provided as the request body. The following optional query parameters are supported:
 - `vl_version`: The Vega-Lite version.
 - `theme`: Named theme as supported by [vega-themes](https://github.com/vega/vega-themes).
 - `scale`: Scale factor for the resulting image size. Defaults to 1.
 - `ppi`: Pixel's per inch of the resulting image. Defaults to 72.

## POST `/api/vl2pdf`
Convert a Vega-Lite spec to a PDF document. The Vega-Lite spec should be provided as the request body. The following optional query parameters are supported:
 - `vl_version`: The Vega-Lite version.
 - `theme`: Named theme as supported by [vega-themes](https://github.com/vega/vega-themes).
 - `scale`: Scale factor for the resulting image size. Defaults to 1.

## POST `/api/vg2svg`
Convert a Vega spec to an SVG image. The Vega spec should be provided as the request body..

## POST `/api/vg2png`
Convert a Vega spec to a PNG image. The Vega spec should be provided as the request body. The following optional query parameters are supported:
 - `scale`: Scale factor for the resulting image size. Defaults to 1.
 - `ppi`: Pixel's per inch of the resulting image. Defaults to 72.

## POST `/api/vg2pdf`
Convert a Vega spec to a PDF document. The Vega spec should be provided as the request body. The following optional query parameters are supported:
 - `scale`: Scale factor for the resulting image size. Defaults to 1.

## Curl usage
Here is an example of converting a Vega-Lite spec to a PNG image using curl. A 2.0 scale factor and dark theme are specified as query parameters.

Example using your self-hosted service:
```bash
curl -X POST "http://localhost:8080/api/vl2png?scale=2.0&theme=dark" \
     -d '{"$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"url": "data/movies.json"}, "mark": "circle", "encoding": {"x": {"bin": {"maxbins": 10}, "field": "IMDB Rating"}, "y": {"bin": {"maxbins": 10}, "field": "Rotten Tomatoes Rating"}, "size": {"aggregate": "count"}}}' \
     -o chart.png
```

# Quick Start

## Using Docker (Recommended)

Build and run the containerized service:

```bash
# Build the Docker image
docker build -t vl-convert-service .

# Run the container
docker run -p 8080:8080 vl-convert-service
```

Or use Docker Compose for easier development:

```bash
# Start the service
docker-compose up

# Stop the service
docker-compose down
```

The service will be available at `http://localhost:8080`

## Local Development

For local development without Docker:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python app.py
```

## Validation

Test the service with the included validation script:

```bash
python verify_migration.py
```

This validates that all endpoints are working correctly and producing the expected responses.