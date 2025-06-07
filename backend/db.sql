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