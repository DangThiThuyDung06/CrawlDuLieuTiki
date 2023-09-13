CREATE database crawl_tiki_panther;
use crawl_tiki_panther;
CREATE TABLE product_info(
  ID_product VARCHAR(100) NOT NULL,
  Product_name NVARCHAR(1000) NULL,
  Price VARCHAR(1000) NULL,
  Classification NVARCHAR(1000) NULL,
  Link VARCHAR(1000) NULL,
  Brand NVARCHAR(1000) NULL,
  PRIMARY KEY (ID_product));
CREATE TABLE history_crawl_data(
  Date_crawl VARCHAR(100) NOT NULL,
  Add_crawl VARCHAR(100) NULL,
  Delete_crawl VARCHAR(100) NULL,
  Update_crawl VARCHAR(100) NULL,
  PRIMARY KEY (Date_crawl));

