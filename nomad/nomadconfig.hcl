datacenter = "dc1"
data_dir   = "/nomad/data/"
bind_addr  = "0.0.0.0"

acl {
  enabled = false
}

client {
  enabled = true
}

server {
  enabled = true
  bootstrap_expect = 1
}
