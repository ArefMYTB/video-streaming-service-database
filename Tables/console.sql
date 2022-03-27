CREATE TABLE `user`
(
    `username`          varchar(255) primary key,
    `name`              varchar(255) NOT NULL,
    `email`             varchar(255) NOT NULL,
    `cellphone`         varchar(11)  NOT NULL,
    `password`          varchar(20) NOT NULL,
    `Introducer`        varchar(255)  NULL,
    `score`             int DEFAULT 0 CHECK (`score` >= 0),
    `amount`            float DEFAULT 0 CHECK ('amount' >= 0 ),
    `Type`              varchar(10) DEFAULT 'typical' CHECK (`Type` in ('typical', 'VIP')),
    `remain_time`       timestamp DEFAULT current_time,
    foreign key (Introducer) references user (username)
    on delete cascade
    on update cascade

);

alter table user
add constraint checkpassword check ( length(password) > 7 and password not like '[a-z]' and password not like '[A-Z]' and password not like '[0-9]') ;

CREATE TABLE `Movie`
(
    `Mid`           int primary key auto_increment,
    `name`          varchar(255) NOT NULL,
    `year`          int  NOT NULL,
    `score`         float DEFAULT 0 CHECK (`score` >= 0),
    `view`          int DEFAULT 0 CHECK (`view` >= 0),
    `price`         float DEFAULT 0 CHECK (`price` >= 0)
);

CREATE TABLE `VIPLists`
(
    `Lid`           int primary key auto_increment,
    `username`      varchar(255) NOT NULL,
    `name`          varchar(255) NOT NULL,
    `status`        varchar(127) CHECK (`status` in ('Private', 'Public', 'Friends')),
    foreign key (username) references user (username)
    on delete cascade
    on update cascade
);

CREATE TABLE `List`
(
    `Lid`           int NOT NULL ,
    `Mid`           int NOT NULL,
    foreign key (Lid) references VIPLists (Lid)
    on delete cascade,
    foreign key (Mid) references Movie (Mid)
    on delete cascade
    on update cascade
);

CREATE TABLE `Friendship`
(
    `username1`           varchar(255) NOT NULL,
    `username2`           varchar(255) NOT NULL,
    `status`              varchar(127) CHECK (`status` in ('accepted', 'in progress', 'denied')),
    foreign key (username1) references user (username)
    on delete cascade
    on update cascade,
    foreign key (username2) references user (username)
    on delete cascade
    on update cascade
);

CREATE TABLE `Comments`
(
    `Mid`            int NOT NULL,
    `username`       varchar(255) NOT NULL,
    `comment`        varchar(500) NOT NULL,
    `score`          int NOT NULL,
    foreign key (Mid) references movie (Mid)
    on delete cascade
    on update cascade,
    foreign key (username) references user (username)
    on delete cascade
    on update cascade
);


CREATE TABLE `Genre`
(
    `Mid`            int NOT NULL ,
    `genre`          varchar(255) NOT NULL,
    foreign key (Mid) references Movie (Mid)
    on delete cascade
    on update cascade
);

CREATE TABLE `Director`
(
    `Mid`            int NOT NULL ,
    `director`       varchar(255) NOT NULL,
    foreign key (Mid) references Movie (Mid)
    on delete cascade
    on update cascade
);

CREATE TABLE `Log`
(
    `username`            varchar(255) NOT NULL,
    `action`              varchar(1000) NOT NULL,
    `time`                timestamp default current_time,
    foreign key (username) references user (username)
    on delete cascade
    on update cascade
);





-- ALTERS
ALTER TABLE comments
ADD CONSTRAINT UQ_UserId_ContactID UNIQUE(username, Mid);


ALTER TABLE log
ADD CONSTRAINT UQ_UserId_ContactID UNIQUE(username, action, time);


ALTER TABLE movie
ADD CONSTRAINT UQ_UserId_ContactID UNIQUE(name, score);


ALTER TABLE friendship
ADD CONSTRAINT UQ_UserId_ContactID UNIQUE(username1, username2);


ALTER TABLE director
ADD CONSTRAINT UQ_UserId_ContactID UNIQUE(Mid,director);


ALTER TABLE genre
ADD CONSTRAINT UQ_UserId_ContactID UNIQUE(Mid,genre);


ALTER TABLE user
ADD CONSTRAINT UQ_UserId_ContactID UNIQUE(email);