terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}


resource "docker_image" "mysql" {
    name         = "mysql"
    keep_locally = true
}

resource "docker_image" "postgres" {
    name         = "postgres"
    keep_locally = true
}

resource "docker_image" "psql" {
  name         = "alpine/psql:latest"
  keep_locally = true
}

#DOCKER IMAGE AS FILE COMPANY FILE DOCKER
/*
resource "docker_image" "flask" {
  name         = "flask"
  keep_locally = true
}
*/


## AS LOCAL DOCKER IMAGE
data "docker_image" "local_image" {
  name = "flask:0.0.2"
}

resource "docker_container" "flask" {

  name  = "FlasAppExaple"

  #DOCKER IMAGE AS FILE COMPANY FILE DOCKER
  #image = "flask"
	#DOCKER IMAGE AS LOCAL FILE
  image = data.docker_image.local_image.name

  ports {

    internal = 5000
    external = 5000

  }
}

resource "docker_container" "postgres" {
image = docker_image.postgres.image_id
name  = "postgres"

  ports {
    internal = 81
    external = 8081
  }

mounts {
    target = "/var/lib/postgresql/data"
    source = "/home/andy/Media/CS/SysAdmin/DetailDrivenManager/pgData"
    type   = "bind"
  }

env = [
    "POSTGRES_PASSWORD=pass",
]
}
