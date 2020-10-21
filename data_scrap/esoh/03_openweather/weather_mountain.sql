CREATE TABLE mt_weather
(
  id         INT(10)     NOT NULL AUTO_INCREMENT,
  mt_id		 INT(10) NOT NULL,
  name       VARCHAR(30) NULL    ,
  temp       VARCHAR(30) NULL     DEFAULT NULL,
  pressure   VARCHAR(30) NULL     DEFAULT NULL,
  humidity   VARCHAR(30) NULL     DEFAULT NULL,
  wind_speed VARCHAR(30) NULL     DEFAULT NULL,
  wind_deg   VARCHAR(30) NULL     DEFAULT NULL,
  clouds     VARCHAR(30) NULL     DEFAULT NULL,
  reg_date   DATE        NULL     DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (mt_id)
  REFERENCES mountains(id)
);