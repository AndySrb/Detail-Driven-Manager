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
    name         = "mysql:8.0.40-bookworm"
    keep_locally = true
}

#DOCKER IMAGE IN DOCKER REPO - TO ADD
/*
resource "docker_image" "flask" {
  name         = "flask"
  keep_locally = true
}
*/


## AS LOCAL DOCKER IMAGE
data "docker_image" "local_image" {
  name = "flask"
}

resource "docker_container" "flask" {

  name  = "FlaskAppExaple"
  #DOCKER IMAGE AS FILE COMPANY FILE DOCKER
  #image = "flask"
	#DOCKER IMAGE AS LOCAL DOCKER FILE
  image = data.docker_image.local_image.name

  ports {

    internal = 5000
    external = 5000

  }
}

resource "docker_container" "mysql" {
image = docker_image.mysql.image_id
name  = "MySQL_Database"

  ports {
    internal = 3306
    external = 3306
  }

mounts {
    target = "/var/lib/mysql"
    source = "/home/andy/Media/CS/SysAdmin/DetailDrivenManager/database" # TODO: Change to local PWD directry or docker volume
    type   = "bind"
  }


  env = [
    "MYSQL_ROOT_PASSWORD=pass",        # TODO: Better password storage
    "MYSQL_DATABASE=mydb",             # Initialize database
    "MYSQL_USER=user",                 # Create a user
    "MYSQL_PASSWORD=pass"              # Set user password
  ]
}
