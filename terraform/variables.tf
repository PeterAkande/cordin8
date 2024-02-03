variable "tags_prefix" {
  type    = string
  default = "dev-cordin8"
}

variable "api_version" {
  default = "v1"
  type    = string
}

variable "python_runtime" {
  type = string
  default = "python3.8"
}