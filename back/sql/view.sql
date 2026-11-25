create or replace view vw_resumen AS
select p.productid,
	   p.productname as product,
	   p.unitprice as price,
	   p.unitsinstock as stock,
	   c.categoryname as category,
	   s.companyname  as supplier,
	   p.discontinued,
	   p.active
	   from products p 
		 join categories c  using (categoryid)
		 join suppliers s using (supplierid)
order by p.productname;


create or replace function fn_filterView(
	p_product varchar default null,
	p_category varchar default null,
	p_discontinued bool default null,
	p_stockmin int default null,
	p_stockmax int default null,
	p_pricemin numeric default null,
	p_pricemax numeric default null
)
returns setof vw_resumen as $$
declare
	stmt varchar;
begin
	-------------------- sentencia base ---------------------------------
	stmt := 'select * from vw_resumen vr where 1 = 1 ';
	if p_product is not null or trim(p_product) <> '' then
	stmt = stmt || format(' and vr.product ILIKE %L','%'|| p_product || '%' );
	end if;
	if p_category is not null or trim(p_category) <> '' then
	   stmt := stmt || format(' and vr.category ILIKE %L','%'||p_category||'%');
	end if;
	if p_discontinued is not null then
	   stmt := stmt || format(' and vr.discontinued = %L',p_discontinued);
	end if;
	
	--- stock 
	if p_stockmin is not null then
		stmt := stmt || format(' and vr.stock <= %L',p_stockmin);
	end if;
	if p_stockmax is not null then
		stmt := stmt || format(' and vr.stock >= %L',p_stockmax);
	end if;
	-- price
	if p_pricemin is not null then		
		stmt := stmt || format(' and vr.price <= %L',p_pricemin);
	end if;
	if p_pricemax is not null then
		stmt := stmt || format(' and vr.price >= %L',p_pricemax);
	end if;

    stmt := stmt || ' order by vr.product';
    return query execute stmt;
end;
$$
language plpgsql;
