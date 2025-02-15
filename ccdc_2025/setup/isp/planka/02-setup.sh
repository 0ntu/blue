psql -c "ALTER USER planka PASSWORD 'DB_PASSWORD_CHANGE_ME';"
cd /var/www/planka
curl -fsSL -O https://github.com/plankanban/planka/releases/latest/download/planka-prebuild.zip
unzip planka-prebuild.zip -d /var/www/
rm planka-prebuild.zip
cd planka
npm install
