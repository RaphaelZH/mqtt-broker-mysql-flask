FROM mysql:latest
RUN export MYSQL_ROOT_PASSWORD=123456
COPY . .
#RUN systemctl start mysqld
RUN mysql -u root -p123456 < ./database.sql
#RUN systemctl stop mysqld
#EXPOSE 3306
#CMD ["mysqld"]