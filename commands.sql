create database iccLab3;
CREATE USER student;
alter user student with encrypted password 'pass';
grant all privileges on database iccLab3 to student;
