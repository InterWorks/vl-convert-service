FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download fonts from CDN, .woff fonts are smaller than .ttf files and more web-optimized
RUN mkdir -p fonts/liberation-mono fonts/liberation-sans fonts/liberation-serif && \
    curl -o fonts/liberation-mono/LiberationMono-Regular.woff https://fonts.cdnfonts.com/s/276/LiberationMono-Regular.woff && \
    curl -o fonts/liberation-mono/LiberationMono-Italic.woff https://fonts.cdnfonts.com/s/276/LiberationMono-Italic.woff && \
    curl -o fonts/liberation-mono/LiberationMono-Bold.woff https://fonts.cdnfonts.com/s/276/LiberationMono-Bold.woff && \
    curl -o fonts/liberation-mono/LiberationMono-BoldItalic.woff https://fonts.cdnfonts.com/s/276/LiberationMono-BoldItalic.woff && \
    curl -o fonts/liberation-sans/LiberationSans-Regular.woff https://fonts.cdnfonts.com/s/277/LiberationSans-Regular.woff && \
    curl -o fonts/liberation-sans/LiberationSans-Italic.woff https://fonts.cdnfonts.com/s/277/LiberationSans-Italic.woff && \
    curl -o fonts/liberation-sans/LiberationSans-Bold.woff https://fonts.cdnfonts.com/s/277/LiberationSans-Bold.woff && \
    curl -o fonts/liberation-sans/LiberationSans-BoldItalic.woff https://fonts.cdnfonts.com/s/277/LiberationSans-BoldItalic.woff && \
    curl -o fonts/liberation-serif/LiberationSerif-Regular.woff https://fonts.cdnfonts.com/s/278/LiberationSerif-Regular.woff && \
    curl -o fonts/liberation-serif/LiberationSerif-Italic.woff https://fonts.cdnfonts.com/s/278/LiberationSerif-Italic.woff && \
    curl -o fonts/liberation-serif/LiberationSerif-Bold.woff https://fonts.cdnfonts.com/s/278/LiberationSerif-Bold.woff && \
    curl -o fonts/liberation-serif/LiberationSerif-BoldItalic.woff https://fonts.cdnfonts.com/s/278/LiberationSerif-BoldItalic.woff

# Copy application code
COPY app.py .

# Create a non-root user with specific UID/GID
RUN groupadd --gid 1000 appuser && \
    useradd --create-home --shell /bin/bash --uid 1000 --gid 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8080

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120", "app:app"]