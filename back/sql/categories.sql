

alter table categories add column discontinued bool default false;


CREATE OR REPLACE FUNCTION fn_trg_bloquear_delete_categorias()
RETURNS trigger AS $$
BEGIN
   RAISE EXCEPTION 'Eliminación física no permitida en categories (ID %). Utilice la baja lógica (discontinued = true) desde el ABM.', OLD.categoryid;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_bloquear_delete_categorias
BEFORE DELETE ON categories
FOR EACH ROW
EXECUTE FUNCTION fn_trg_bloquear_delete_categorias();


CREATE OR REPLACE FUNCTION fn_trg_am_categorias()
RETURNS trigger AS $$
BEGIN
   NEW.categoryname := trim(coalesce(NEW.categoryname, ''));
   IF NEW.categoryname = '' THEN
       RAISE EXCEPTION 'El nombre de la categoría no puede estar vacío.';
   END IF;
   IF EXISTS (
       SELECT 1
       FROM categories
       WHERE lower(trim(categoryname)) = lower(NEW.categoryname)
         AND (TG_OP = 'INSERT' OR categoryid <> NEW.categoryid)
   ) THEN
       RAISE EXCEPTION 'Ya existe una categoría con el nombre "%".', NEW.categoryname;
   END IF;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_am_categorias
BEFORE INSERT OR UPDATE ON categories
FOR EACH ROW
EXECUTE FUNCTION fn_trg_am_categorias();



CREATE or REPLACE FUNCTION fn_abmr_categorias(
	p_accion text, p_id text, p_nombre text,
	p_descripcion text, p_imagen text)
RETURNS text as $$
DECLARE
	v_accion text;
	v_id_num integer;
	v_discontinued boolean;
BEGIN
	-- 1. Validar acción
	IF p_accion IS NULL OR trim(p_accion) = '' THEN
       RAISE EXCEPTION 'Debe indicar una acción (A, B, M o R).';
   END IF;
   v_accion := upper(trim(p_accion));
   IF v_accion NOT IN ('A', 'B', 'M', 'R') THEN
       RAISE EXCEPTION 'Acción inválida: %. Use A, B, M o R.', v_accion;
   END IF;
   -- 2. Validar y convertir ID cuando corresponde a M, B o R
   IF v_accion IN ('M', 'B', 'R') THEN
       IF p_id IS NULL OR trim(p_id) = '' THEN
           RAISE EXCEPTION 'Debe indicar un ID de categoría para la acción %.', v_accion;
       END IF;
       BEGIN
           v_id_num := trim(p_id)::integer;
       EXCEPTION WHEN invalid_text_representation THEN
           RAISE EXCEPTION 'El ID de categoría "%" no es un número válido.', p_id;
       END;
       SELECT discontinued
       INTO v_discontinued
       FROM categories
       WHERE categoryid = v_id_num;
       IF NOT FOUND THEN
           RAISE EXCEPTION 'No existe la categoría con ID %.', v_id_num;
       END IF;
   END IF;
   -- 3. Ejecutar según acción
	CASE v_accion
		WHEN 'A' THEN
			INSERT INTO categories (categoryname, description, picture)
           VALUES (p_nombre, p_descripcion, p_imagen);
           RETURN 'Categoría dada de alta correctamente.';
			
		WHEN 'B' THEN
			--Solo necesito el id, chequear que exista, que no este dada de baja y luego cambiar discontinued a true
			IF v_discontinued = true THEN
               RAISE EXCEPTION 'La categoría con ID % ya se encuentra dada de baja.', v_id_num;
           END IF;
           UPDATE categories
           SET discontinued = true
           WHERE categoryid = v_id_num;
           RETURN 'Categoría dada de baja correctamente.';
		WHEN 'M' THEN
			IF v_discontinued THEN
               RAISE EXCEPTION 'No se puede modificar la categoría con ID % porque está dada de baja.', v_id_num;
           END IF;
			UPDATE categories
           SET categoryname = p_nombre,
               description  = p_descripcion,
               picture      = p_imagen
           WHERE categoryid = v_id_num;
           RETURN 'Categoría modificada correctamente.';
		WHEN 'R' THEN
           IF NOT v_discontinued THEN
               RAISE EXCEPTION 'La categoría con ID % ya se encuentra activa.', v_id_num;
           END IF;
           UPDATE categories
           SET discontinued = false
           WHERE categoryid = v_id_num;
           RETURN 'Categoría reactivada correctamente.';
		END CASE;
END;
$$ LANGUAGE plpgsql;







