FROM python:3.10 AS base

# Ensure Python logs are unbuffered
ENV PYTHONUNBUFFERED 1

# Accept ARG for unprivileged Django user (not currently used, consider adding later)
ARG DJANGO_UNPRIVILEGED_USER

# Update system and set locale
RUN apt update && apt upgrade --yes && \
    apt-get install -y locales locales-all && \
    rm -rf /var/lib/apt/lists/*

# Set locale to German
ENV LANG de_DE.UTF-8  
ENV LANGUAGE de_DE:de  
ENV LC_ALL de_DE.UTF-8  


FROM base AS dev
WORKDIR /analyticDashboardDjangoApp/
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
