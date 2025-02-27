INSERT INTO issued_status(issued_id, issued_member_id, issued_book_name, issued_date, issued_book_isbn, issued_emp_id)
VALUES
('IS151', 'C118', 'The Catcher in the Rye', CURRENT_DATE - INTERVAL '24 days',  '978-0-553-29698-2', 'E108'),
('IS152', 'C119', 'The Catcher in the Rye', CURRENT_DATE - INTERVAL '13 days',  '978-0-553-29698-2', 'E109'),
('IS153', 'C106', 'Pride and Prejudice', CURRENT_DATE - INTERVAL '7 days',  '978-0-14-143951-8', 'E107'),
('IS154', 'C105', 'The Road', CURRENT_DATE - INTERVAL '32 days',  '978-0-375-50167-0', 'E101');

ALTER TABLE return_status
ADD Column book_quality VARCHAR(15) DEFAULT('Good');

UPDATE return_status
SET book_quality = 'Damaged'
WHERE issued_id 
    IN ('IS112', 'IS117', 'IS118');
SELECT * FROM return_status;

Select * from books;
Select * from branch;
Select * from members;
Select * from issued_status;
Select * from return_status;
Select * from employees;

--1. Overdue period
Select ist.issued_member_id,m.member_name, bk.book_title, ist.issued_date,current_date- issued_date as days_overdue from issued_status as ist
join members as m
on ist.issued_member_id=m.member_id
join books as bk
on bk.isbn=ist.issued_book_isbn
left join return_status as rs
on rs.issued_id=ist.issued_id
where return_id is null
and current_date- issued_date >30
order by 1

--2. Branch performance report
create table branch_performance as
Select b.branch_id,b.manager_id, sum(bk.rental_price)as total_revenue, count(ist.issued_id)as books_issued, count(rs.return_id)as books_returned
from issued_status as ist join
employees as e on
ist.issued_emp_id=e.emp_id join
branch as b on
b.branch_id=e.branch_id
left join return_status as rs
on rs.issued_id=ist.issued_id
join books as bk
on ist.issued_book_isbn=bk.isbn
group by 1,2

--3. Active members

Create table active_members as
select m.member_id, m.member_name,m.member_address
from members as m
join issued_status as ist
on m.member_id=ist.issued_member_id
where issued_date> current_date-interval '6 months'

--4. Top 3 Employees with most books
Select e.emp_name,count(ist.issued_id)as books_issued,b.branch_id,b.branch_address from employees as e
join issued_status as ist
on e.emp_id=ist.issued_emp_id
join branch as b 
on b.branch_id=e.branch_id
group by e.emp_name,b.branch_id
order by books_issued desc
limit 3

--5. Stored procedure on Book availability

select* from books;
select * from issued_status;

create or replace procedure book_issue(p_issued_id varchar(10),p_issued_member_id varchar(30),p_issued_book_isbn varchar(30),p_issued_emp_id varchar(30))
language plpgsql 
as
$$

declare
v_status varchar(10);

begin
select status 
into v_status 
from
books
where isbn=p_issued_book_isbn;

if v_status='yes' then

insert into issued_status(issued_id,issued_member_id,issued_date,issued_book_isbn,issued_emp_id)
values (p_issued_id,p_issued_member_id,current_date,p_issued_book_isbn,p_issued_emp_id);

Update books
set status='no'
where isbn=p_issued_book_isbn;

Raise notice 'Book added succesfully for isbn:%', p_issued_book_isbn;

else

Raise notice 'Book not available for book isbn:%', p_issued_book_isbn;
end if;
end;
$$

call book_issue('IS155','C108','978-0-553-29698-2','E104');

