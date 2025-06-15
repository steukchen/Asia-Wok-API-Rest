
BEGIN; 

	WITH new_register AS (
	  INSERT INTO users (username, email,rol,password)
<<<<<<< HEAD
	  VALUES ('HARSUE', 'HARWINGMR@GMAIL.COM','superadmin','$argon2id$v=19$m=65536,t=3,p=4$sr+pkKUTFRsQ2oDT1cRZ8A$X+7bgXsqrUBccVR8WiXmO2ITVCNps/BPyP/bxBGl8y0')
=======
	  VALUES ('HARSUE', 'HARWINGMR@GMAIL.COM','superadmin','RELAMPAGOARRASA')
>>>>>>> 147ca99600ffaf02067ed69480dd9120e5fd12f0
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
	VALUES (1,'BS',96),(2,'COP',3800);

	INSERT INTO tables (id,name)
	VALUES (1,'MESA 1'),(2,'MESA 2'),(3,'MESA 3');

	INSERT INTO orders(id,customer_id,created_by,table_id)
	VALUES (1,1,uuid(current_setting('app.user_id')),1);

	INSERT INTO order_dishes(order_id,dish_id,quantity)
	VALUES (1,1,2),(1,2,1);

	INSERT INTO order_currencies(order_id,currency_id,quantity)
	VALUES (1,2,29640);
	

COMMIT; 