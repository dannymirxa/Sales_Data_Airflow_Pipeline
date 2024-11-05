```bash
docker run --name mysql-diy --network diy_network -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=diy -e MYSQL_USER=myuser -e MYSQL_PASSWORD=mypassword mysql:8.0.40-debian
```