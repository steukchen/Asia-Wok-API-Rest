CREATE OR REPLACE FUNCTION change_update_at()
RETURNS TRIGGER AS $$
BEGIN
	NEW.updated_at = NOW();	
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER tr_update_at
BEFORE UPDATE ON currencies
FOR EACH ROW EXECUTE FUNCTION change_update_at();

CREATE OR REPLACE TRIGGER tr_update_at
BEFORE UPDATE ON customers
FOR EACH ROW EXECUTE FUNCTION change_update_at();

CREATE OR REPLACE TRIGGER tr_update_at
BEFORE UPDATE ON dishes
FOR EACH ROW EXECUTE FUNCTION change_update_at();

CREATE OR REPLACE TRIGGER tr_update_at
BEFORE UPDATE ON dishes_types
FOR EACH ROW EXECUTE FUNCTION change_update_at();

CREATE OR REPLACE TRIGGER tr_update_at
BEFORE UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION change_update_at();

CREATE OR REPLACE TRIGGER tr_update_at
BEFORE UPDATE ON tables
FOR EACH ROW EXECUTE FUNCTION change_update_at();

CREATE OR REPLACE TRIGGER tr_update_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION change_update_at();


CREATE OR REPLACE FUNCTION log_order_currencies_audit()
RETURNS TRIGGER AS $$
BEGIN
	NEW.updated_at = NOW();
	IF TG_OP = 'UPDATE' THEN
		INSERT INTO order_currencies_audit (order_id,action,old_data,new_data,changed_by)
		VALUES (old.order_id,'updated',
			jsonb_build_object('id',old.id,'currency_id',old.currency_id,'quantity',old.quantity),
			jsonb_build_object('id',new.id,'currency_id',new.currency_id,'quantity',new.quantity),
			current_setting('app.current_user_id', TRUE)::uuid
		);
	ELSIF TG_OP = 'DELETE' THEN
		INSERT INTO order_currencies_audit (order_id,action,old_data,new_data,changed_by)
		VALUES (old.order_id,'deleted',
			jsonb_build_object('id',old.id,'currency_id',old.currency_id,'quantity',old.quantity),
			jsonb_build_object('id',old.id),
			current_setting('app.current_user_id', TRUE)::uuid
		);
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER tr_log_order_currencies
BEFORE UPDATE OR DELETE ON order_currencies
FOR EACH ROW EXECUTE FUNCTION log_order_currencies_audit();


CREATE OR REPLACE FUNCTION log_order_dishes_audit()
RETURNS TRIGGER AS $$
BEGIN
	NEW.updated_at = NOW();
	IF TG_OP = 'UPDATE' THEN
		INSERT INTO order_dishes_audit (order_id,action,old_data,new_data,changed_by)
		VALUES (old.order_id,'updated',
			jsonb_build_object('id',old.id,'dish_id',old.dish_id,'quantity',old.quantity),
			jsonb_build_object('id',new.id,'dish_id',new.dish_id,'quantity',new.quantity),
			current_setting('app.current_user_id', TRUE)::uuid
		);
	ELSIF TG_OP = 'DELETE' THEN
		INSERT INTO order_dishes_audit (order_id,action,old_data,new_data,changed_by)
		VALUES (old.order_id,'deleted',
			jsonb_build_object('id',old.id,'dish_id',old.dish_id,'quantity',old.quantity),
			jsonb_build_object('id',old.id),
			current_setting('app.current_user_id', TRUE)::uuid
		);
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER tr_log_order_dishes
BEFORE UPDATE OR DELETE ON order_dishes
FOR EACH ROW EXECUTE FUNCTION log_order_dishes_audit();