
-- VALIDAR CAMPOS DEL PRODUCTO --


create or replace function fntg_validateproduct()
returns trigger as 
$$
begin

	-- Normalizar textos para luego validar
    new.productname     := btrim(new.productname);
    new.quantityperunit := btrim(new.quantityperunit);
    
    -- Validar primero si el nombre es nulo o vacio
    if new.productname = '' or new.productname is null then
        raise exception 'productname es obligatorio y no puede estar en blanco';
    end if;

	-- validar si existe otro producto con ese nombre en un INSERT o UPDATE
	if exists (
		select 1 from products p
		where lower(btrim(p.productname)) = lower(new.productname)
		  and (TG_OP = 'INSERT' or p.productid <> new.productid)
	) then
		raise exception 'Ya existe un producto con el nombre %', new.productname;
	end if;
	
	-- validar si el proveedor existe
	if not exists (select 1 from suppliers s where s.supplierid = new.supplierid) then
        raise exception 'El proveedor % no existe', new.supplierid;
    end if;
	
	-- validar si el proveedor que se quiere insertar o actualizar esta dado de baja
	if (TG_OP = 'INSERT' 
		or new.supplierid is distinct from old.supplierid
		or (new.active and not old.active)
		or (old.discontinued and not new.discontinued)
		)
	    and exists (select 1 from suppliers s
	                where s.supplierid = new.supplierid and s.active = false) then
		raise exception 'El proveedor % está dado de baja', new.supplierid;
	end if;

	-- validar si la categoria existe 
    if not exists (select 1 from categories c where c.categoryid = new.categoryid) then
        raise exception 'La categoría % no existe', new.categoryid;
    end if;


 	-- validar campos       
    if new.quantityperunit = '' or new.quantityperunit is null then 
		raise exception 'quantityperunit es obligatorio y  no puede estar en blanco';
	end if;
	if  new.unitprice < 0 or new.unitprice is null then
		raise exception 'unitprice es obligatorio y debe ser mayor o igual a 0';
	end if;
	if  new.unitsinstock < 0 or new.unitsinstock is null then
		raise exception 'units es obligatorio y debe ser mayor o igual a 0';
	end if;
	if  new.reorderlevel < 0 or new.reorderlevel is null then 
		raise exception 'reorderlevel es obligatorio y debe ser mayor o igual a 0';
	end if; 
	if  new.unitsonorder < 0 or new.unitsonorder is null then
		raise exception 'unitsinorder es obligatorio y debe ser mayor o igual a 0';
	end if;
	
	
	-- reglas de actualizacion
	if TG_OP = 'UPDATE' then
	
		if old.discontinued and new.unitsinstock > old.unitsinstock then
		
			raise exception 'El producto esta descontinuado, no se puede agregar más stock.';
			
		end if;
		
		if old.discontinued and new.unitsonorder > old.unitsonorder then
		
			raise exception 'El producto esta descontinuado, no se puede agregar más unidades en orden.';
		
		end if;
		
		if not old.active and 
			( new.unitsinstock <> old.unitsinstock or
			  new.unitsonorder <> old.unitsonorder ) then
			  
			raise exception 'El producto esta dado de baja, no admite movimientos';
			
		end if;
		
	
	 end if;
	
		
	return new;
	 	
end;
$$
language plpgsql;


create trigger tg_validateproduct before insert or update
on products for each row execute function fntg_validateproduct();

-------------------------------------------------------------------


create or replace function fn_insertProduct(
							p_productname varchar,
							p_supplierid int,
							p_categoryid int,
							p_quantityperunit varchar,
							p_unitprice numeric,
							p_unitsinstock int,
							p_unitsonorder int,
							p_reorderlevel int
)
returns products as $$
declare 

	v_product record;
	
begin
    
		INSERT INTO products (
		productname,
		supplierid,
		categoryid,
		quantityperunit,
		unitprice,
		unitsinstock,
		unitsonorder,
		reorderlevel)
		values (
		p_productname,
		p_supplierid,
		p_categoryid,
		p_quantityperunit,
		p_unitprice,
		p_unitsinstock,
		p_unitsonorder,
		p_reorderlevel)
		returning * into v_product;
	
	return v_product;

end;
$$
language plpgsql;



------------------------------------------------------------------------------------

-- UPDATE --

create or replace function fn_updateProduct(
							p_productid int,
							p_productname varchar,
							p_supplierid int,
							p_categoryid int,
							p_quantityperunit varchar,
							p_unitprice numeric,
							p_unitsinstock int,
							p_unitsonorder int,
							p_reorderlevel int,
							p_discontinued bool)
returns products as $$
declare 

	v_product record;
	
begin

		select * into v_product from products p
		where p.productid = p_productid; 
		
		IF NOT FOUND THEN
        	RAISE EXCEPTION 'No existe el producto';
    	END IF;
    	
    	if not v_product.active then
    		
    		raise exception 'El producto esta dado de baja, debes darlo de alta';
    	
    	end if;

		UPDATE products 
		set productname = p_productname,
		supplierid = p_supplierid,
		categoryid = p_categoryid,
		quantityperunit= p_quantityperunit,
		unitprice = p_unitprice,
		unitsinstock = p_unitsinstock,
		unitsonorder = p_unitsonorder,
		reorderlevel = p_reorderlevel,
	    discontinued = p_discontinued
		where productid = p_productid
		returning * into v_product;
	
		return v_product;
end;
$$
language plpgsql;


----------------------------------------------------------------------

-- DELETE --


create or replace function fn_deleteproduct(p_productid int)
returns products as $$
declare
	v_product record;
begin


	select * into v_product from products p
	where p.productid = p_productid and
	p.active = true
	for update;
	
	
	if not found then
	
		raise exception 'Producto no encontrado';
		
	end if;
	
 

	if v_product.unitsinstock > 0 or v_product.unitsonorder > 0 then
	
		raise exception 'El producto % todavia tiene unidades en stock', v_product.productname;
		
	end if;

	
	UPDATE products
	SET active = false
	WHERE productid = p_productid 
	RETURNING * INTO v_product;
	
	
	return v_product;
	
end;
$$
language plpgsql;



-- dar de alta el producto

create or replace function fn_activateproduct(p_productid int)
returns products as $$
declare

	v_product record;
	
begin
	
	select * into v_product from products p
	where p.productid = p_productid;
	
	
	if not found then
	
		raise exception 'El Producto no existe';
	
	end if;
	
	if v_product.active then 
	
		return v_product;
	
	end if;
	
	if not exists (
		select 1 from suppliers s 
		where s.supplierid = v_product.supplierid 
		and s.active = true) then
		
		raise exception 'El proveedor esta dado de baja, debes activarlo';
	
	end if;
	

	update products
	set active = true
	where productid = p_productid
	returning * into v_product;
	
	return v_product;
	
end;
$$
language plpgsql;











