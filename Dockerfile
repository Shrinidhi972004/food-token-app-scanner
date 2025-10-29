# Multi-stage build for Food Token Scanner
# Stage 1: Base image with Node.js and Python
FROM node:18-bullseye-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python3-tk \
    build-essential \
    curl \
    dumb-init \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN groupadd -r nodejs && useradd -r -g nodejs nodejs

# Set working directory
WORKDIR /app

# Stage 2: Install dependencies
FROM base as dependencies

# Copy package files
COPY package*.json ./
COPY requirements.txt ./

# Install Node.js dependencies
RUN npm ci --only=production && npm cache clean --force

# Create Python virtual environment and install dependencies
RUN python3 -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 3: Production image
FROM base as production

# Copy Node.js dependencies from dependencies stage
COPY --from=dependencies /app/node_modules ./node_modules

# Copy Python virtual environment from dependencies stage
COPY --from=dependencies /app/.venv ./.venv

# Copy application code
COPY --chown=nodejs:nodejs . .

# Create necessary directories
RUN mkdir -p uploads qr_codes_jpeg qr-codes database logs public && \
    chown -R nodejs:nodejs /app

# Make Python venv available in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# Start command
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]
