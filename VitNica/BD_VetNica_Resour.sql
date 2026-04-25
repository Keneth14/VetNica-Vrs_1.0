Create Database VetNica_Resour
go

Use VetNica_Resour
go

-- =========================
-- TABLA: animals
-- =========================
CREATE TABLE animals (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    age_type VARCHAR(10) NOT NULL 
        CONSTRAINT chk_age_type CHECK (age_type IN ('Años', 'Meses')),
    owner VARCHAR(100) NOT NULL
);

-- =========================
-- TABLA: records (historial médico)
-- =========================
CREATE TABLE records (
    id INT PRIMARY KEY IDENTITY(1,1),
    animal_id INT NOT NULL,
    record_type VARCHAR(50) NOT NULL, -- vacuna, desparasitacion, diagnostico, tratamiento
    description VARCHAR(255),
    date DATE DEFAULT GETDATE(),

    FOREIGN KEY (animal_id) REFERENCES animals(id)
);

-- =========================
-- TABLA: alerts
-- =========================
CREATE TABLE alerts (
    id INT PRIMARY KEY IDENTITY(1,1),
    animal_id INT NOT NULL,
    message VARCHAR(255),
    alert_date DATE,
    status VARCHAR(50) DEFAULT 'pending',

    FOREIGN KEY (animal_id) REFERENCES animals(id)
);

-- =========================
-- TABLA: invoices
-- =========================
CREATE TABLE invoices (
    id INT PRIMARY KEY IDENTITY(1,1),
    client_name VARCHAR(100) NOT NULL,
    animal_id INT NULL,
    description VARCHAR(255),
    price DECIMAL(10,2) NOT NULL,
    date DATE DEFAULT GETDATE(),

    FOREIGN KEY (animal_id) REFERENCES animals(id)
);

-- =========================
-- TRIGGER: alert por tratamiento
-- =========================
CREATE TRIGGER trg_create_alert
ON records
AFTER INSERT
AS
BEGIN
    INSERT INTO alerts (animal_id, message, alert_date)
    SELECT 
        i.animal_id,
        'Retiro de medicamento: no consumir productos por 3 dias',
        DATEADD(DAY, 3, GETDATE())
    FROM inserted i
    WHERE LOWER(i.record_type) = 'tratamiento'
END;

-- =========================
-- TRIGGER: validar edad
-- =========================
CREATE TRIGGER trg_validate_age
ON animals
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM inserted WHERE age < 0)
    BEGIN
        RAISERROR ('Error: edad no válida', 16, 1);
        RETURN;
    END

    INSERT INTO animals (name, type, age, age_type, owner)
    SELECT name, type, age, age_type, owner
    FROM inserted;
END;

-- =========================
-- TRIGGER: alerta vacuna
-- =========================
CREATE TRIGGER trg_vaccine_alert
ON records
AFTER INSERT
AS
BEGIN
    INSERT INTO alerts (animal_id, message, alert_date)
    SELECT 
        i.animal_id,
        'Proxima vacuna en 30 dias',
        DATEADD(DAY, 30, GETDATE())
    FROM inserted i
    WHERE LOWER(i.record_type) = 'vacuna'
END;

-- =========================
-- TRIGGER: estado alertas
-- =========================
CREATE TRIGGER trg_update_alert_status
ON alerts
AFTER INSERT
AS
BEGIN
    UPDATE alerts
    SET status = 'expired'
    WHERE alert_date < GETDATE();
END;


ALTER TRIGGER trg_validate_age
ON animals
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM inserted WHERE age < 0)
    BEGIN
        RAISERROR ('Error: edad no válida', 16, 1);
        RETURN;
    END

    INSERT INTO animals (name, type, age, age_type, owner)
    SELECT name, type, age, age_type, owner
    FROM inserted;
END;


ALTER TABLE invoices
ADD animal_id INT;

ALTER TABLE invoices
ADD CONSTRAINT fk_invoices_animals
FOREIGN KEY (animal_id) REFERENCES animals(id);

ALTER TABLE invoices
DROP COLUMN animal_name;

select * from invoices;

