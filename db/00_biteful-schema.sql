CREATE DATABASE IF NOT EXISTS biteful;

USE biteful;
GRANT ALL PRIVILEGES ON biteful TO 'webapp'@'%';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS Diner (
    firstName varchar(40),
    lastName varchar(40),
    bio varchar(400),
    email varchar(40) UNIQUE,
    dinerID int PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Administrator (
    firstName varchar(40),
    lastName varchar(40),
    phoneNumber varchar(15),
    email varchar(40) UNIQUE,
    adminID int PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Restaurant (
    name varchar(100),
    approved bool DEFAULT false,
    openingTime varchar(15),
    closingTime varchar(15),
    phoneNumber varchar(15),
    takeout bool,
    dineIn bool,
    website varchar(100),
    cuisine varchar(50),
    address varchar(100),
    images varchar(100),
    restaurantID int PRIMARY KEY,
    adminID int,

    CONSTRAINT fk_1
        FOREIGN KEY (adminID) REFERENCES Administrator(adminID)
            ON UPDATE restrict ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS Bookmark (
    restaurantID int,
    dinerID int,
    PRIMARY KEY(restaurantID, dinerID),

    CONSTRAINT fk_2
        FOREIGN KEY (restaurantID) REFERENCES Restaurant(restaurantID)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT fk_3
        FOREIGN KEY (dinerID) REFERENCES Diner(dinerID)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS MenuItem (
    currentlyAvailable bool,
    calories int,
    description varchar(300),
    name varchar(40),
    price int,
    vegan bool,
    dairyFree bool,
    glutenFree bool,
    allergies varchar(100),
    chefsChoice bool,
    popular bool,
    type varchar(50),
    itemID int,
    restaurantID int,
    PRIMARY KEY(itemID, restaurantID),

    CONSTRAINT fk_4
        FOREIGN KEY (restaurantID) REFERENCES Restaurant(restaurantID)
            ON UPDATE restrict ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS Review (
    text varchar(500),
    timeStamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    price int,
    rating int,
    images varchar(100),
    reviewID int PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS ReviewDetails (
    reviewID int,
    dinerID int,
    PRIMARY KEY(dinerID, reviewID),
    CONSTRAINT fk_5
        FOREIGN KEY (dinerID) REFERENCES Diner(dinerID)
            ON UPDATE restrict ON DELETE restrict,
    CONSTRAINT fk_6
        FOREIGN KEY (reviewID) REFERENCES Review(reviewID)
            ON UPDATE restrict ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS Owner (
    firstName varchar(40),
    lastName varchar(40),
    phoneNumber varchar(15),
    email varchar(40) UNIQUE,
    ownerID int PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS OwnerDetails (
    ownerID int,
    restaurantID int,
    PRIMARY KEY(ownerID, restaurantID),
    CONSTRAINT fk_7
        FOREIGN KEY (ownerID) REFERENCES Owner(ownerID)
            ON UPDATE restrict ON DELETE restrict,
    CONSTRAINT fk_8
        FOREIGN KEY (restaurantID) REFERENCES Restaurant(restaurantID)
            ON UPDATE restrict ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS ReviewFlags (
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    reviewedByAdmin bool DEFAULT false,
    description varchar(200),
    reviewID int,
    ownerID int,
    adminID int,
    PRIMARY KEY(ownerID, reviewID, adminID),
    CONSTRAINT fk_9
        FOREIGN KEY (ownerID) REFERENCES Owner(ownerID)
                               ON UPDATE restrict ON DELETE restrict,
    CONSTRAINT fk_10
        FOREIGN KEY (reviewID) REFERENCES Review(reviewID)
                               ON UPDATE restrict ON DELETE restrict,
    CONSTRAINT fk_11
        FOREIGN KEY (adminID) REFERENCES Administrator(adminID)
                               ON UPDATE restrict ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS Critic (
    firstName varchar(40),
    lastName varchar(40),
    bio varchar(400),
    email varchar(40) UNIQUE,
    reviewCount int,
    criticID int PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Curation (
    reviewID int,
    criticID int,
    PRIMARY KEY(reviewID, criticID),
    CONSTRAINT fk_12
        FOREIGN KEY (reviewID) REFERENCES Review(reviewID)
            ON UPDATE restrict ON DELETE restrict,
    CONSTRAINT fk_13
        FOREIGN KEY (criticID) REFERENCES Critic(criticID)
            ON UPDATE restrict ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS Nomination (
    month varchar(20),
    criticID int,
    restaurantID int,
    PRIMARY KEY(month, criticID, restaurantID),
    CONSTRAINT fk_14
        FOREIGN KEY (criticID) REFERENCES Critic(criticID)
            ON UPDATE restrict ON DELETE restrict,
    CONSTRAINT fk_15
        FOREIGN KEY (restaurantID) REFERENCES Restaurant(restaurantID)
            ON UPDATE restrict ON DELETE restrict
);
       