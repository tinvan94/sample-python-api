 select name 
 from customers 
 where dob = (select max(dob) from customers)
 