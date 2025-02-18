curl https://go.dev/dl/go1.24.0.linux-amd64.tar.gz -o
tar -xf go1.24.0.linux-amd64.tar.gz
rm go1.24.0.linux-amd64.tar.gz

curl https://github.com/caddyserver/xcaddy/releases/download/v0.4.4/xcaddy_0.4.4_linux_amd64.tar.gz -o
tar -xf xcaddy_0.4.4_linux_amd64.tar.gz
rm xcaddy_0.4.4_linux_amd64.tar.gz

xcaddy build --with github.com/corazawaf/coraza-caddy/v2
