from flask import Flask, request, Response, jsonify
from pathlib import Path
import vl_convert as vlc
import json
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure VlConvert
ALLOWED_BASE_URLS = ["https://vega.github.io/vega-datasets/"]
vlc.register_font_directory(str(Path("fonts").absolute()))

def handle_conversion_error(e):
    """Handle conversion exceptions consistently"""
    response = Response(f"conversion failed: {str(e)}", status=400, mimetype="text/plain")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

def handle_successful_conversion(content, content_type):
    """Handle successful conversions consistently"""
    response = Response(content, mimetype=content_type)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response

@app.route('/api/vl2png', methods=['OPTIONS'])
@app.route('/api/vl2svg', methods=['OPTIONS'])
@app.route('/api/vl2pdf', methods=['OPTIONS'])
@app.route('/api/vl2vg', methods=['OPTIONS'])
@app.route('/api/vg2png', methods=['OPTIONS'])
@app.route('/api/vg2svg', methods=['OPTIONS'])
@app.route('/api/vg2pdf', methods=['OPTIONS'])
def options_handler():
    """Handle preflight OPTIONS requests"""
    response = Response(status=204)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response

@app.route('/api/version', methods=['GET'])
def version():
    """Returns VlConvert version info"""
    return Response(vlc.__version__, mimetype="text/plain")

@app.route('/api/vl2vg', methods=['POST'])
def vl2vg():
    """Vega-Lite spec → Vega spec"""
    # Check content length like the original implementation
    content_len = int(request.headers.get("Content-Length", 0))
    if content_len == 0:
        response = Response("POST body must be a Vega-Lite spec", status=400, mimetype="text/plain")
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    vl_spec = request.get_data(as_text=True)
    vl_version = request.args.get("vl_version")

    try:
        vg_spec = vlc.vegalite_to_vega(vl_spec, vl_version=vl_version)
        return handle_successful_conversion(json.dumps(vg_spec).encode(), "application/json")
    except Exception as e:
        return handle_conversion_error(e)

@app.route('/api/vl2svg', methods=['POST'])
def vl2svg():
    """Vega-Lite spec → SVG image"""
    # Check content length like the original implementation
    content_len = int(request.headers.get("Content-Length", 0))
    if content_len == 0:
        response = Response("POST body must be a Vega-Lite spec", status=400, mimetype="text/plain")
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    vl_spec = request.get_data(as_text=True)
    vl_version = request.args.get("vl_version")
    theme = request.args.get("theme")

    try:
        svg = vlc.vegalite_to_svg(
            vl_spec,
            vl_version=vl_version,
            theme=theme,
            allowed_base_urls=ALLOWED_BASE_URLS,
        )
        return handle_successful_conversion(svg.encode(), "image/svg+xml")
    except Exception as e:
        return handle_conversion_error(e)

@app.route('/api/vl2png', methods=['POST'])
def vl2png():
    """Vega-Lite spec → PNG image"""
    # Check content length like the original implementation
    content_len = int(request.headers.get("Content-Length", 0))
    if content_len == 0:
        response = Response("POST body must be a Vega-Lite spec", status=400, mimetype="text/plain")
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    vl_spec = request.get_data(as_text=True)
    vl_version = request.args.get("vl_version")
    scale = request.args.get("scale")
    ppi = request.args.get("ppi")
    theme = request.args.get("theme")

    try:
        png_data = vlc.vegalite_to_png(
            vl_spec,
            vl_version=vl_version,
            scale=float(scale) if scale is not None else None,
            ppi=float(ppi) if ppi is not None else None,
            theme=theme,
            allowed_base_urls=ALLOWED_BASE_URLS,
        )
        return handle_successful_conversion(png_data, "image/png")
    except Exception as e:
        return handle_conversion_error(e)

@app.route('/api/vl2pdf', methods=['POST'])
def vl2pdf():
    """Vega-Lite spec → PDF document"""
    # Check content length like the original implementation
    content_len = int(request.headers.get("Content-Length", 0))
    if content_len == 0:
        response = Response("POST body must be a Vega-Lite spec", status=400, mimetype="text/plain")
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    vl_spec = request.get_data(as_text=True)
    vl_version = request.args.get("vl_version")
    scale = request.args.get("scale")
    ppi = request.args.get("ppi")
    theme = request.args.get("theme")

    try:
        pdf_data = vlc.vegalite_to_pdf(
            vl_spec,
            vl_version=vl_version,
            scale=float(scale) if scale is not None else None,
            ppi=float(ppi) if ppi is not None else None,
            theme=theme,
            allowed_base_urls=ALLOWED_BASE_URLS,
        )
        return handle_successful_conversion(pdf_data, "application/pdf")
    except Exception as e:
        return handle_conversion_error(e)

@app.route('/api/vg2svg', methods=['POST'])
def vg2svg():
    """Vega spec → SVG image"""
    # Check content length like the original implementation
    content_len = int(request.headers.get("Content-Length", 0))
    if content_len == 0:
        response = Response("POST body must be Vega spec", status=400, mimetype="text/plain")
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    vg_spec = request.get_data(as_text=True)
    theme = request.args.get("theme")

    try:
        svg = vlc.vega_to_svg(
            vg_spec,
            theme=theme,
            allowed_base_urls=ALLOWED_BASE_URLS,
        )
        return handle_successful_conversion(svg.encode(), "image/svg+xml")
    except Exception as e:
        return handle_conversion_error(e)

@app.route('/api/vg2png', methods=['POST'])
def vg2png():
    """Vega spec → PNG image"""
    # Check content length like the original implementation
    content_len = int(request.headers.get("Content-Length", 0))
    if content_len == 0:
        response = Response("POST body must be Vega spec", status=400, mimetype="text/plain")
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    vg_spec = request.get_data(as_text=True)
    scale = request.args.get("scale")
    ppi = request.args.get("ppi")
    theme = request.args.get("theme")

    try:
        png_data = vlc.vega_to_png(
            vg_spec,
            scale=float(scale) if scale is not None else None,
            ppi=float(ppi) if ppi is not None else None,
            theme=theme,
            allowed_base_urls=ALLOWED_BASE_URLS,
        )
        return handle_successful_conversion(png_data, "image/png")
    except Exception as e:
        return handle_conversion_error(e)

@app.route('/api/vg2pdf', methods=['POST'])
def vg2pdf():
    """Vega spec → PDF document"""
    # Check content length like the original implementation
    content_len = int(request.headers.get("Content-Length", 0))
    if content_len == 0:
        response = Response("POST body must be Vega spec", status=400, mimetype="text/plain")
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    vg_spec = request.get_data(as_text=True)
    scale = request.args.get("scale")
    ppi = request.args.get("ppi")
    theme = request.args.get("theme")

    try:
        pdf_data = vlc.vega_to_pdf(
            vg_spec,
            scale=float(scale) if scale is not None else None,
            ppi=float(ppi) if ppi is not None else None,
            theme=theme,
            allowed_base_urls=ALLOWED_BASE_URLS,
        )
        return handle_successful_conversion(pdf_data, "application/pdf")
    except Exception as e:
        return handle_conversion_error(e)

if __name__ == '__main__':
    # Run HTTP service - SSL will be handled by reverse proxy in production
    app.run(host='0.0.0.0', port=8080, debug=False)