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
      version = "~> 6.0"
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

resource "google_storage_bucket" "sample" {
  name                        = var.bucket_name
  location                    = "US"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false

  labels = {
    env   = "dev"
    owner = "platform"
    app   = "terraform-plan-reviewer-test"
  }
}

output "bucket_name" {
  value = google_storage_bucket.sample.name
}
