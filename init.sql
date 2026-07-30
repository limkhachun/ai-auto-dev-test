-- ============================================================
-- Super Admin Dashboard — Database Initialisation Script
-- Target: MySQL 8.0+
-- ============================================================

CREATE DATABASE IF NOT EXISTS `test_ai_db`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE `test_ai_db`;

-- ============================================================
-- 1. Users (accounts with role-based access)
-- ============================================================
CREATE TABLE IF NOT EXISTS `users` (
    `id`            INT             NOT NULL AUTO_INCREMENT,
    `username`      VARCHAR(50)     NOT NULL,
    `email`         VARCHAR(120)    NOT NULL,
    `password_hash` VARCHAR(255)    NOT NULL,
    `role`          VARCHAR(20)     NOT NULL DEFAULT 'user'
                    COMMENT 'Enum: user, staff, superadmin',
    `created_at`    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`),
    UNIQUE KEY `uk_email` (`email`),
    KEY `idx_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 2. Products (inventory)
-- ============================================================
CREATE TABLE IF NOT EXISTS `products` (
    `id`            INT             NOT NULL AUTO_INCREMENT,
    `name`          VARCHAR(200)    NOT NULL,
    `description`   TEXT            NULL,
    `price`         DECIMAL(10,2)   NOT NULL DEFAULT 0.00,
    `stock`         INT             NOT NULL DEFAULT 0,
    `created_at`    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_name` (`name`),
    KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 3. Orders (order headers)
-- ============================================================
CREATE TABLE IF NOT EXISTS `orders` (
    `id`            INT             NOT NULL AUTO_INCREMENT,
    `user_id`       INT             NOT NULL,
    `total_amount`  DECIMAL(12,2)   NOT NULL DEFAULT 0.00,
    `status`        VARCHAR(20)     NOT NULL DEFAULT 'pending'
                    COMMENT 'Enum: pending, paid, shipped',
    `created_at`    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_status` (`status`),
    KEY `idx_created_at` (`created_at`),
    CONSTRAINT `fk_orders_user` FOREIGN KEY (`user_id`)
        REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 4. Order Items (line items within an order)
-- ============================================================
CREATE TABLE IF NOT EXISTS `order_items` (
    `id`            INT             NOT NULL AUTO_INCREMENT,
    `order_id`      INT             NOT NULL,
    `product_id`    INT             NOT NULL,
    `quantity`      INT             NOT NULL DEFAULT 1,
    `price`         DECIMAL(10,2)   NOT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_order_id` (`order_id`),
    KEY `idx_product_id` (`product_id`),
    CONSTRAINT `fk_order_items_order` FOREIGN KEY (`order_id`)
        REFERENCES `orders` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_order_items_product` FOREIGN KEY (`product_id`)
        REFERENCES `products` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 5. Audit Logs (staff operation trail)
-- ============================================================
CREATE TABLE IF NOT EXISTS `audit_logs` (
    `id`                INT             NOT NULL AUTO_INCREMENT,
    `staff_id`          INT             NOT NULL,
    `action_description` VARCHAR(500)   NOT NULL,
    `target_type`       VARCHAR(50)     NULL
                        COMMENT 'e.g. product, order, staff',
    `created_at`        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_staff_id` (`staff_id`),
    KEY `idx_target_type` (`target_type`),
    KEY `idx_created_at` (`created_at`),
    CONSTRAINT `fk_audit_logs_staff` FOREIGN KEY (`staff_id`)
        REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Optional: Seed a default superadmin account
--   username: admin
--   password: admin123
-- ============================================================
-- INSERT INTO `users` (`username`, `email`, `password_hash`, `role`)
-- VALUES (
--     'admin',
--     'admin@example.com',
--     -- This is the Werkzeug hash for 'admin123' (generated at runtime)
--     -- Use the app to register or generate via Python:
--     --   from werkzeug.security import generate_password_hash
--     --   print(generate_password_hash('admin123'))
--     'scrypt:32768:8:1$...',
--     'superadmin'
-- );
