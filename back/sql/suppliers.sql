

create or replace function fntg_validatesupplier()
returns trigger as
$$
begin
	-- Normaliza textos, convierte '' en null
	new.companyname := nullif(btrim(new.companyname), '');
	new.contactname := nullif(btrim(new.contactname), '');
	new.contacttitle:= nullif(btrim(new.contacttitle), '');
	new.address := nullif(btrim(new.address), '');
	new.city := nullif(btrim(new.city), '');
	new.region := nullif(btrim(new.region), '');
	new.postalcode := nullif(btrim(new.postalcode), '');
	new.country := nullif(btrim(new.country), '');
	new.phone := nullif(btrim(new.phone), '');
	new.fax := nullif(btrim(new.fax), '');
	new.homepage := nullif(btrim(new.homepage), '');

	-- Campos obligatorios
	if new.companyname is null then
		raise exception 'companyname es obligatorio';
	end if;
	if new.contactname is null then
		raise exception 'contactname es obligatorio';
	end if;
	if new.contacttitle is null then
		raise exception 'contacttitle es obligatorio';
	end if;
	if new.address is null then
		raise exception 'address es obligatorio';
	end if;
	if new.city is null then
		raise exception 'city es obligatorio';
	end if;
	if new.region is null then
		raise exception 'region es obligatorio';
	end if;
	if new.postalcode is null then
		raise exception 'postalcode es obligatorio';
end if;
	if new.country is null then
		raise exception 'country es obligatorio';
	end if;

	if new.phone is null then
		raise exception 'phone es obligatorio';
	end if;
	if new.fax is null then
		raise exception 'fax es obligatorio';
	end if;
	if new.homepage is null then
		raise exception 'homepage es obligatorio';
	end if;
	-- Nombre de empresa único
	if exists (
		select 1 from suppliers s
		where lower(s.companyname) = lower(new.companyname)
		  and s.supplierid <> new.supplierid
	) then
		raise exception 'Ya existe un proveedor con el nombre %', new.companyname;
	end if;
	-- Formato de phone
	if new.phone !~ '^[0-9 +()-]+$' then
		raise exception 'phone tiene un formato invalido';
	end if;

	return new;
end;
$$
language plpgsql;


create trigger tg_validatesupplier before insert or update
on suppliers for each row execute function fntg_validatesupplier();


create or replace function fn_insertsupplier(
	p_companyname varchar,
	p_contactname varchar,
	p_contacttitle varchar,
	p_address varchar,
	p_city varchar,
	p_region varchar,
	p_postalcode varchar,
	p_country varchar,
	p_phone varchar,
	p_fax varchar,
	p_homepage text)
returns suppliers as $$
declare
	v_supplier record;
begin
	insert into suppliers (
		companyname, contactname, contacttitle, address, city,
		region, postalcode, country, phone, fax, homepage)
	values (
		p_companyname, p_contactname, p_contacttitle, p_address, p_city,
		p_region, p_postalcode, p_country, p_phone, p_fax, p_homepage)
	returning * into v_supplier;
	return v_supplier;
end;
$$
language plpgsql;


create or replace function fn_updatesupplier(
	p_supplierid int,
	p_companyname varchar,
	p_contactname varchar,
	p_contacttitle varchar,
	p_address varchar,
	p_city varchar,
	p_region varchar,
	p_postalcode varchar,
	p_country varchar,
	p_phone varchar,
	p_fax varchar,
	p_homepage text)
returns suppliers as $$
declare
	v_supplier record;
begin
	update suppliers
		set companyname = p_companyname,
			contactname = p_contactname,
			contacttitle = p_contacttitle,
			address = p_address,
			city = p_city,
			region  = p_region,
			postalcode= p_postalcode,
			country= p_country,
			phone= p_phone,
			fax= p_fax,
			homepage= p_homepage
	where supplierid = p_supplierid
	  and active = true
	returning * into v_supplier;

	if not found then
		raise exception 'No existe el proveedor %', p_supplierid;
	end if;

	return v_supplier;
end;
$$
language plpgsql;



create or replace function fn_deletesupplier(p_supplierid int)
returns suppliers as $$
declare
	v_supplier record;
begin
	select * into v_supplier from suppliers s
	where s.supplierid = p_supplierid
	  and s.active = true
	for update;

	if not found then
		raise exception 'Proveedor con id % no encontrado', p_supplierid;
	end if;

	-- sus productos se discontinuan y se cancelan los pedidos pendientes
	update products
	set discontinued = true,
	    unitsonorder = 0
	where supplierid = p_supplierid;

	update suppliers
	set active = false
	where supplierid = p_supplierid
	returning * into v_supplier;

	return v_supplier;
end;
$$
language plpgsql;


create or replace function fn_activatesupplier(p_supplierid int)
returns suppliers as $$
declare
	v_supplier record;
begin
	select * into v_supplier from suppliers s
	where s.supplierid = p_supplierid
	for update;

	if not found then
		raise exception 'El proveedor no existe';
	end if;

	if v_supplier.active then
		return v_supplier;
	end if;

	update suppliers
	set active = true
	where supplierid = p_supplierid
	returning * into v_supplier;

	return v_supplier;
end;
$$
language plpgsql;











