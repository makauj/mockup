-- This SQL script creates a table named 'collections' with various fields and constraints.
-- It includes a foreign key reference to another table named 'other_table'.
CREATE TABLE if not exists collections (
    record_id SERIAL PRIMARY KEY,             -- Unique identifier for each row
    ID INTEGER NOT NULL,                      -- Foreign key (still validated)
    Name TEXT,
    Email TEXT,
    Contact TEXT,
    Date DATE DEFAULT CURRENT_DATE,
    read_only BOOLEAN DEFAULT FALSE,
    last_updated_by TEXT,
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (ID) REFERENCES other_table(id)
);

CREATE OR REPLACE FUNCTION prevent_update_on_readonly()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.read_only THEN
        RAISE EXCEPTION 'Row % is read-only and cannot be modified', OLD.record_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_update_on_readonly
BEFORE UPDATE ON collections
FOR EACH ROW
EXECUTE FUNCTION prevent_update_on_readonly();

CREATE OR REPLACE FUNCTION set_audit_fields()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated_at := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_audit_fields
BEFORE INSERT OR UPDATE ON collections
FOR EACH ROW
EXECUTE FUNCTION set_audit_fields();