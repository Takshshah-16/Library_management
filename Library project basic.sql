select * from books;
select * from branch;
select * from members;
select * from issued_status;
select * from return_status;
select * from employees;

--1. Insert into books a new record

insert into books values
(
'978-1-60129-456-2','To Kill a Mockingbird','Classic',6.00,'yes','Harper Lee','J.B Lippincot & Co.'
);
select * from books;




--2. Updating a record from members table

Update Members
Set member_address='125 Main St'
Where member_id='C101';

select * from members;

3. Delete a record from issued status where issue id is 107

Delete from issued_status
where issued_id='IS107';
select * from issued_status;

--4. Retrieve books issued by employee id 101

Select * from issued_status
where issued_emp_id='E101';

--5. List members who have issued more than one book

with number_of_books as
(select issued_emp_id, count(issued_book_name)as number
from issued_status
group by issued_emp_id)

select issued_emp_id from number_of_books
where number>1;

--6. Count of books issued based on each book title

create table book_counts as
select b.book_title, count(i.issued_id)as number_of_books_issued
from books as b
join issued_status as i
on b.isbn=i.issued_book_isbn
group by b.book_title
order by b.book_title;

select * from book_counts;

--7. Retrieve all books in a specific category(Classic books)

Select * 
from books
where category='Classic';

--8. Find total rental income by category

Select b.category, sum(b.rental_price)as total_rental_price
from books as b join issued_status as i
on b.isbn=i.issued_book_isbn
group by b.category;

--9. Employee with thei branch details

Select * from branch;
select * from employees;

select e1.*, b.manager_id, e2.emp_name from employees as e1
join branch as b
on e1.branch_id=b.branch_id
join employees as e2
on b.manager_id=e2.emp_id;

--10. Table of books with rental price greater than 7

Create table book_prices_greater_than_7 as
Select book_title, rental_price
from books
where rental_price >7;


--11. Books that have not been returned
select * from issued_status;
select * from return_status;

select i.issued_book_name from issued_status as i
left join return_status as rs
on i.issued_id=rs.issued_id
where rs.return_id is null;


