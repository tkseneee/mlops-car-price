##############################################################
# 1) Use a lightweight official Python base image
# ------------------------------------------------------------
# python:3.10-slim is a very small Debian-based Python image.
# Perfect for Streamlit apps because:
#   - It reduces image size
#   - Starts up faster in serverless environments
##############################################################
FROM python:3.10-slim


##############################################################
# 2) Set environment variables
# ------------------------------------------------------------
# PYTHONUNBUFFERED=1 → prints logs in real-time (important for debugging)
# PIP_NO_CACHE_DIR=1 → prevents pip from storing cached wheels (saves space)
# DEBIAN_FRONTEND=noninteractive → avoids tz/keyboard prompts when installing packages
##############################################################
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive


##############################################################
# 3) Set the working directory inside the container
# ------------------------------------------------------------
# All subsequent commands (RUN/COPY/CMD) will be executed inside /app.
##############################################################
WORKDIR /app


##############################################################
# 4) OPTIONAL: Install OS-level dependencies
# ------------------------------------------------------------
# Most Python packages (numpy, pandas, sklearn) already ship wheels.
# If your image builds WITHOUT these, comment this block out.
#
# build-essential is only required for compiling packages from source.
##############################################################
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*


##############################################################
# 5) Copy only requirements first
# ------------------------------------------------------------
# Docker cache optimization:
# If requirements.txt doesn't change, Docker will reuse the pip install layer.
##############################################################
COPY requirements.txt .


##############################################################
# 6) Install Python dependencies
# ------------------------------------------------------------
# --no-cache-dir ensures smaller image size.
# Requirements include: streamlit, pandas, numpy, sklearn, joblib, protobuf
##############################################################
RUN pip install --no-cache-dir -r requirements.txt


##############################################################
# 7) Copy application code
# ------------------------------------------------------------
# These are the ONLY files needed at runtime:
#   - Streamlit UI script
#   - Custom transformer (for unpickling)
#   - Saved sklearn pipeline (.pkl)
##############################################################
COPY app.py .
COPY custom_transformers.py .
COPY car_price_pipeline.pkl .


##############################################################
# 8) Expose Streamlit's default port
# ------------------------------------------------------------
# Streamlit always runs on port 8501 unless overridden.
##############################################################
EXPOSE 8501


##############################################################
# 9) Start the Streamlit app
# ------------------------------------------------------------
# Streamlit MUST listen on 0.0.0.0 inside Docker,
# otherwise Azure Container Apps / Docker port mapping won't work.
##############################################################
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
