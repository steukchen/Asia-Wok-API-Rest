
BEGIN; 

	WITH new_register AS (
		INSERT INTO users (username, email,rol,password)
		VALUES ('HARSUE', 'HARWINGMR@GMAIL.COM','superadmin','RELAMPAGOARRASA')
		RETURNING id
	)
	SELECT SET_CONFIG('app.user_id', id::TEXT, true)
	FROM new_register;
	
	INSERT INTO customers (id,ci,name,lastname,phone_number,address)
	VALUES (1,'V32325849','HARWING','MARTINEZ','04161797833','EL PALMAR');

	INSERT INTO dishes_types(id,name) 
	VALUES (1,'COMIDA'),(2,'BEBIDA');
	
	INSERT INTO dishes(id,name,description,price,type_id)
	VALUES 
	(1,'ARROZ ESPECIAL','NOSEPO MEN',3.40,1),
	(2,'COCA COLA','NOSEPO MENX2',2,2);

	INSERT INTO currencies(id,name,exchange)
	VALUES (1,'DOLAR',1),(2,'BS',96),(3,'COP',3800);

	INSERT INTO tables (id,name)
	VALUES (1,'MESA 1'),(2,'MESA 2'),(3,'MESA 3');

	INSERT INTO orders(id,customer_id,created_by,table_id)
	VALUES (1,1,uuid(current_setting('app.user_id')),1);

	INSERT INTO order_dishes(order_id,dish_id,quantity,price)
	VALUES (1,1,2,3.40),(1,2,1,2.2);

	INSERT INTO order_currencies(order_id,currency_id,quantity,exchange)
	VALUES (1,3,29640,3800);
	

COMMIT; 