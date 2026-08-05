# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de

RUN pip install --no-cache-dir --only-binary :all: uv==0.8.13

WORKDIR /code

RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --home-dir /code app

COPY ./pyproject.toml ./README.md ./uv.lock ./

COPY ./app ./app

RUN uv sync --frozen --no-install-project --no-build && chown -R app:app /code

ARG COMMIT_SHA=""
ENV COMMIT_SHA=${COMMIT_SHA}

ARG AGENT_VERSION=0.0.0
ENV AGENT_VERSION=${AGENT_VERSION}

EXPOSE 8080

USER 10001:10001

CMD ["uv", "run", "--no-sync", "--no-build", "uvicorn", "app.fast_api_app:app", "--host", "0.0.0.0", "--port", "8080"]
