FROM ghcr.io/astral-sh/uv:python3.13-alpine

RUN --mount=from=ghcr.io/astral-sh/uv:0.4.24,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    # psycopg runtime dep
    apk add --no-cache libpq libpq postgresql-client \
    # export requirements from uv.lock since uv does not support sync without venv
    && uv export --frozen --format requirements-txt --no-dev --quiet | uv pip install --system -r -

WORKDIR /src
COPY src .

RUN : \
    && mkdir /home/website \
    && mkdir /home/website/statics \
    && mkdir /home/website/media \
    && mkdir /home/website/logs

# removes \r from script and makes it executable.
# both of these are caused by windows users touching file and not configuring git properly
RUN : \
    && sed -i 's/\r//g' entrypoint.sh \
    && chmod +x entrypoint.sh

ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]