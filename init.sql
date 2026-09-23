CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    email VARCHAR(50)
);

INSERT INTO usuarios (nombre, email) VALUES 
('Juan Perez', 'juan@example.com'), 
('Maria Gomez', 'maria@example.com'),
('Carlos Ruiz', 'carlos@example.com');
