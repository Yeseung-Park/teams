-- 데이터베이스 초기화 스크립트

-- Store 테이블 생성
CREATE TABLE IF NOT EXISTS stores (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    store_identifier VARCHAR(50) UNIQUE NOT NULL,
    admin_username VARCHAR(50) NOT NULL,
    admin_password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 테이블 생성
CREATE TABLE IF NOT EXISTS tables (
    table_id INT AUTO_INCREMENT PRIMARY KEY,
    store_id INT NOT NULL,
    table_number INT NOT NULL,
    table_password_hash VARCHAR(255) NOT NULL,
    current_session_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    UNIQUE KEY unique_store_table (store_id, table_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TableSession 테이블 생성
CREATE TABLE IF NOT EXISTS table_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    table_id INT NOT NULL,
    session_start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end_time TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (table_id) REFERENCES tables(table_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Category 테이블 생성
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    store_id INT NOT NULL,
    category_name VARCHAR(50) NOT NULL,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES stores(store_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Menu 테이블 생성
CREATE TABLE IF NOT EXISTS menus (
    menu_id INT AUTO_INCREMENT PRIMARY KEY,
    store_id INT NOT NULL,
    category_id INT NOT NULL,
    menu_name VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    display_order INT DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Order 테이블 생성
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    store_id INT NOT NULL,
    table_id INT NOT NULL,
    session_id INT NOT NULL,
    order_number VARCHAR(20) NOT NULL,
    total_amount INT NOT NULL,
    order_status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    FOREIGN KEY (table_id) REFERENCES tables(table_id),
    FOREIGN KEY (session_id) REFERENCES table_sessions(session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- OrderItem 테이블 생성
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_id INT NOT NULL,
    menu_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    unit_price INT NOT NULL,
    subtotal INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (menu_id) REFERENCES menus(menu_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 초기 데이터 삽입

-- 1. 매장 생성 (비밀번호: admin123)
INSERT INTO stores (store_name, store_identifier, admin_username, admin_password_hash) VALUES
('테스트 레스토랑', 'STORE001', 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewiV7u2uV7u2uV7u');

-- 2. 테이블 생성 (비밀번호: table123)
INSERT INTO tables (store_id, table_number, table_password_hash) VALUES
(1, 1, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewiV7u2uV7u2uV7u'),
(1, 2, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewiV7u2uV7u2uV7u'),
(1, 3, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewiV7u2uV7u2uV7u'),
(1, 4, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewiV7u2uV7u2uV7u'),
(1, 5, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewiV7u2uV7u2uV7u');

-- 3. 카테고리 생성
INSERT INTO categories (store_id, category_name, display_order) VALUES
(1, '메인 요리', 1),
(1, '사이드 메뉴', 2),
(1, '음료', 3);

-- 4. 샘플 메뉴 생성
INSERT INTO menus (store_id, category_id, menu_name, price, description, display_order, is_available) VALUES
(1, 1, '김치찌개', 8000, '얼큰한 김치찌개', 1, TRUE),
(1, 1, '된장찌개', 7000, '구수한 된장찌개', 2, TRUE),
(1, 1, '불고기', 15000, '달콤한 불고기', 3, TRUE),
(1, 1, '비빔밥', 9000, '영양 가득 비빔밥', 4, TRUE),
(1, 1, '냉면', 10000, '시원한 냉면', 5, TRUE),
(1, 1, '삼겹살', 18000, '고소한 삼겹살', 6, TRUE),
(1, 2, '공기밥', 1000, '흰쌀밥', 1, TRUE),
(1, 3, '콜라', 2000, '시원한 콜라', 1, TRUE),
(1, 3, '사이다', 2000, '시원한 사이다', 2, TRUE);
