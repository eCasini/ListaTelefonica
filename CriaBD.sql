CREATE TABLE Area (
    id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    nome  TEXT UNIQUE,
    ramal INTEGER  
);

CREATE TABLE SubArea (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    nome  TEXT UNIQUE,
    ramal INTEGER,
    area_id  INTEGER
);

-- DROP TABLE Area;
-- DROP TABLE SubArea
