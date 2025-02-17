psql -c "ALTER USER planka PASSWORD 'DB_PASSWORD_CHANGE_ME';"
cd /tmp
curl -fsSL -O https://github.com/plankanban/planka/releases/latest/download/planka-prebuild.zip
unzip planka-prebuild.zip -d /var/www/
cd /var/www/planka
rm planka-prebuild.zip
cd planka
npm install
