cat << EOF
metadata_dir = "/var/lib/garage/meta"
data_dir = "/var/lib/garage/data"

db_engine = "lmdb"

#block_size = 1048576

replication_mode = "none"

#compression_level = 1

rpc_secret = "$(openssl rand -hex 32)"
rpc_bind_addr = "[::]:3901"
#rpc_public_addr = "[fc00:3::1]:3901"

#bootstrap_peers = [
#  "$(openssl rand -hex 32)@[fc00:1::1]:3901",
#  "$(openssl rand -hex 32)@[fc00:2::2]:3901",
#  "$(openssl rand -hex 32)@[fc00:b::1]:3901",
#  "$(openssl rand -hex 32)@[fc00:b::2]:3901",
#]

[s3_api]
api_bind_addr = "[::]:3900"
s3_region = "garage"
root_domain = ".s3.garage.localhost"

[s3_web]
bind_addr = "[::]:3902"
root_domain = ".web.garage.localhost"
index = "index.html"

[admin]
api_bind_addr = "[::]:3903"
metrics_token = "$(openssl rand -base64 32)"
admin_token = "$(openssl rand -base64 32)"
EOF
