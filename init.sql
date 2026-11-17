CREATE TABLE IF NOT EXISTS emergency_calls (
    id SERIAL PRIMARY KEY,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    description TEXT,
    zip_code VARCHAR(20),
    title VARCHAR(255),
    category VARCHAR(50),
    call_subtype VARCHAR(150),
    time_stamp TIMESTAMP,
    township VARCHAR(100),
    address VARCHAR(255)
);

CREATE INDEX IF NOT EXISTS idx_calls_timestamp ON emergency_calls (time_stamp);
CREATE INDEX IF NOT EXISTS idx_calls_category ON emergency_calls (category);
CREATE INDEX IF NOT EXISTS idx_calls_zip ON emergency_calls (zip_code);