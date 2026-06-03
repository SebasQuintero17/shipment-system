-- 2. Script para insertar datos y visualizarlos
INSERT INTO couriers (name, vehicle_plate) VALUES 
('Juan Perez', 'XYZ-123'),
('Ana Gomez', 'ABC-987');

INSERT INTO shipments (tracking_number, status, destination) VALUES 
('TRK-1001', 'PENDING', 'Bogota'),
('TRK-1002', 'IN_TRANSIT', 'Medellin');

-- Visualizar los datos
SELECT * FROM couriers;
SELECT * FROM shipments;
