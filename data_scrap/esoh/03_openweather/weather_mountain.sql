
CREATE TABLE weather_mountain
(
  id         INT(10)     NOT NULL AUTO_INCREMENT,
  name       VARCHAR(30) NULL    ,
  temp       VARCHAR(30) NULL     DEFAULT NULL,
  pressure   VARCHAR(30) NULL     DEFAULT NULL,
  humidity   VARCHAR(30) NULL     DEFAULT NULL,
  wind_speed VARCHAR(30) NULL     DEFAULT NULL,
  wind_deg   VARCHAR(30) NULL     DEFAULT NULL,
  clouds     VARCHAR(30) NULL     DEFAULT NULL,
  reg_date   DATE        NULL     DEFAULT NULL,
  PRIMARY KEY (id)
);
