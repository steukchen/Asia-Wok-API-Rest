BEGIN;
	SET LOCAL app.current_user_id TO '64a6805e-5236-40af-a4b8-3242b914d24d';
	DELETE FROM order_currencies WHERE ID=1;
COMMIT;