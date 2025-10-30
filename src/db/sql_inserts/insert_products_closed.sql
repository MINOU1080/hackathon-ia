USE ing;

CREATE TABLE IF NOT EXISTS `products_closed` (`product_id` TEXT, `customer_id` TEXT, `product_type` TEXT, `product_name` TEXT, `opened_date` TEXT, `status` TEXT);

INSERT INTO `products_closed` (`product_id`, `customer_id`, `product_type`, `product_name`, `opened_date`, `status`) VALUES ('2051', '1001', 'Credit Card', 'ING Visa Classic', '2012-01-15', 'Closed');
INSERT INTO `products_closed` (`product_id`, `customer_id`, `product_type`, `product_name`, `opened_date`, `status`) VALUES ('2052', '1002', 'Investment Account', 'ING Invest', '2015-06-20', 'Closed');
INSERT INTO `products_closed` (`product_id`, `customer_id`, `product_type`, `product_name`, `opened_date`, `status`) VALUES ('2053', '1003', 'Savings Account', 'ING Savings', '2016-08-10', 'Closed');
INSERT INTO `products_closed` (`product_id`, `customer_id`, `product_type`, `product_name`, `opened_date`, `status`) VALUES ('2054', '1004', 'Credit Card', 'ING Visa Gold', '2014-03-25', 'Closed');
INSERT INTO `products_closed` (`product_id`, `customer_id`, `product_type`, `product_name`, `opened_date`, `status`) VALUES ('2055', '1005', 'Personal Loan', 'ING Personal Loan', '2021-01-10', 'Closed');
INSERT INTO `products_closed` (`product_id`, `customer_id`, `product_type`, `product_name`, `opened_date`, `status`) VALUES ('2056', '1008', 'Investment Account', 'ING Invest', '2019-05-15', 'Closed');
INSERT INTO `products_closed` (`product_id`, `customer_id`, `product_type`, `product_name`, `opened_date`, `status`) VALUES ('2057', '1009', 'Personal Loan', 'ING Personal Loan', '2017-11-20', 'Closed');
INSERT INTO `products_closed` (`product_id`, `customer_id`, `product_type`, `product_name`, `opened_date`, `status`) VALUES ('2058', '1010', 'Savings Account', 'ING Savings', '2013-04-30', 'Closed');
INSERT INTO `products_closed` (`product_id`, `customer_id`, `product_type`, `product_name`, `opened_date`, `status`) VALUES ('2059', '1031', 'Credit Card', 'ING Visa Classic', '2015-09-15', 'Closed');
INSERT INTO `products_closed` (`product_id`, `customer_id`, `product_type`, `product_name`, `opened_date`, `status`) VALUES ('2060', '1032', 'Personal Loan', 'ING Personal Loan', '2019-07-12', 'Closed');
