terraform {
  required_version = "1.15.7"

  cloud {
    organization = "devops_vv"

    workspaces {
      name = "agents"
    }
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.40"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "bucket_name" {
  type = string
}

variable "log_bucket_name" {
  description = "Name of an existing GCS bucket that receives access logs."
  type        = string
}

resource "google_storage_bucket_iam_member" "log_writer" {
  bucket = var.log_bucket_name
  role   = "roles/storage.objectCreator"
  member = "group:cloud-storage-analytics@google.com"
}

resource "google_storage_bucket" "sample" {
  name                        = var.bucket_name
  location                    = "US"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false

  logging {
    log_bucket        = var.log_bucket_name
    log_object_prefix = "access-logs"
  }

  labels = {
    env   = "dev"
    owner = "platform"
    app   = "terraform-plan-reviewer-test"
  }

  depends_on = [google_storage_bucket_iam_member.log_writer]
}

output "bucket_name" {
  value = google_storage_bucket.sample.name
}
