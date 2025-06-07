-- This SQL script creates a table named 'collections' with various fields and constraints.
-- It includes a foreign key reference to another table named 'other_table'.
CREATE TABLE collections (
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
        RAISE EXCEPTION 'This row is read-only and cannot be updated';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_readonly_before_update
BEFORE UPDATE ON collections
FOR EACH ROW
EXECUTE FUNCTION prevent_update_on_readonly();

CREATE OR REPLACE FUNCTION update_audit_fields()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated_at = CURRENT_TIMESTAMP;
    -- Assume the application sets current_user for 'last_updated_by'
    IF NEW.last_updated_by IS NULL THEN
        NEW.last_updated_by = current_user;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_audit_on_change
BEFORE UPDATE ON collections
FOR EACH ROW
WHEN (OLD.* IS DISTINCT FROM NEW.*)
EXECUTE FUNCTION update_audit_fields();