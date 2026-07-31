#!/usr/bin/env bash
set -euo pipefail

settings_file="${1:-.github/container-release.settings}"
repository="${2:-}"

if [[ ! -f "$settings_file" ]]; then
  echo "Settings file not found: $settings_file" >&2
  exit 1
fi

read_setting() {
  local name="$1"
  sed -n "s/^${name}=//p" "$settings_file" | tail -n 1
}

sonar_host_url="$(read_setting SONAR_HOST_URL)"
sonar_organization="$(read_setting SONAR_ORGANIZATION)"
sonar_token="$(read_setting SONAR_TOKEN)"
dockerhub_username="$(read_setting DOCKERHUB_USERNAME)"
dockerhub_repository="$(read_setting DOCKERHUB_REPOSITORY)"
dockerhub_token="$(read_setting DOCKERHUB_TOKEN)"
wif_provider="$(read_setting WIF_PROVIDER)"
wif_service_account="$(read_setting WIF_SERVICE_ACCOUNT)"
google_cloud_project="$(read_setting GOOGLE_CLOUD_PROJECT)"
anthropic_api_key="$(read_setting ANTHROPIC_API_KEY)"

require_real_value() {
  local name="$1"
  local value="$2"
  if [[ -z "$value" || "$value" == REPLACE_ME* ]]; then
    echo "Replace the placeholder for $name in $settings_file" >&2
    exit 1
  fi
}

require_real_value SONAR_HOST_URL "$sonar_host_url"
require_real_value SONAR_ORGANIZATION "$sonar_organization"
require_real_value SONAR_TOKEN "$sonar_token"
require_real_value DOCKERHUB_USERNAME "$dockerhub_username"
require_real_value DOCKERHUB_REPOSITORY "$dockerhub_repository"
require_real_value DOCKERHUB_TOKEN "$dockerhub_token"
require_real_value WIF_PROVIDER "$wif_provider"
require_real_value WIF_SERVICE_ACCOUNT "$wif_service_account"
require_real_value GOOGLE_CLOUD_PROJECT "$google_cloud_project"

gh auth status --hostname github.com >/dev/null

if [[ -z "$repository" ]]; then
  repository="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"
fi

printf '%s' "$sonar_token" | gh secret set SONAR_TOKEN --repo "$repository"
printf '%s' "$sonar_organization" | gh secret set SONAR_ORGANIZATION --repo "$repository"
printf '%s' "$dockerhub_token" | gh secret set DOCKERHUB_TOKEN --repo "$repository"
printf '%s' "$sonar_host_url" | gh secret set SONAR_HOST_URL --repo "$repository"
printf '%s' "$dockerhub_username" | gh secret set DOCKERHUB_USERNAME --repo "$repository"
printf '%s' "$dockerhub_repository" | gh secret set DOCKERHUB_REPOSITORY --repo "$repository"
printf '%s' "$wif_provider" | gh secret set WIF_PROVIDER --repo "$repository"
printf '%s' "$wif_service_account" | gh secret set WIF_SERVICE_ACCOUNT --repo "$repository"
printf '%s' "$google_cloud_project" | gh secret set GOOGLE_CLOUD_PROJECT --repo "$repository"

anthropic_configured=false
if [[ -n "$anthropic_api_key" && "$anthropic_api_key" != REPLACE_ME* ]]; then
  printf '%s' "$anthropic_api_key" | gh secret set ANTHROPIC_API_KEY --repo "$repository"
  anthropic_configured=true
fi

echo "Configured GitHub Actions settings for $repository:"
echo "- required pipeline secrets and identifiers configured"
if [[ "$anthropic_configured" == true ]]; then
  echo "- optional ANTHROPIC_API_KEY configured"
else
  echo "- optional ANTHROPIC_API_KEY skipped"
fi
