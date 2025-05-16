-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS ph_agua;

-- Usar o banco criado
USE ph_agua;

-- Criação da tabela de medições
CREATE TABLE IF NOT EXISTS medicoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ph_valor FLOAT NOT NULL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
