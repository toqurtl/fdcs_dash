-- Database setup script for AdminLTE Dashboard

-- Create database
CREATE DATABASE IF NOT EXISTS dashboard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dashboard;

-- Users table for authentication
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Business categories table
CREATE TABLE business_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    `order` INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Business contents table
CREATE TABLE business_contents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    route VARCHAR(100) NOT NULL,
    icon VARCHAR(50),
    `order` INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES business_categories(id) ON DELETE CASCADE
);

-- Insert sample data
INSERT INTO users (username, email, password_hash) VALUES 
('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6lUYBWMnNG'); -- password: admin123

INSERT INTO business_categories (name, description, `order`) VALUES
('영업관리', '영업 관련 업무를 관리합니다', 1),
('재무관리', '재무 관련 업무를 관리합니다', 2),
('인사관리', '인사 관련 업무를 관리합니다', 3);

INSERT INTO business_contents (category_id, name, route, icon, `order`) VALUES
(1, '매출현황', 'sales', 'fas fa-chart-line', 1),
(1, '고객분석', 'customers', 'fas fa-users', 2),
(1, '영업기회', 'opportunities', 'fas fa-handshake', 3),
(2, '수익분석', 'profit', 'fas fa-dollar-sign', 1),
(2, '비용관리', 'expenses', 'fas fa-receipt', 2),
(2, '예산계획', 'budget', 'fas fa-calculator', 3),
(3, '직원관리', 'employees', 'fas fa-user-tie', 1),
(3, '급여관리', 'payroll', 'fas fa-money-check-alt', 2),
(3, '성과평가', 'performance', 'fas fa-star', 3);