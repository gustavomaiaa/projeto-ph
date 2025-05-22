ALTER TABLE usuarios MODIFY senha_hash VARCHAR(255);
SHOW CREATE TABLE usuarios;
DESCRIBE usuarios;
ALTER TABLE usuarios MODIFY senha_hash VARCHAR(512) NULL;

