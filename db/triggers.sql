-- ==========================================
-- ТРИГГЕРЫ (TRIGGERS)
-- ==========================================

-- 1. Логирование изменений заказов в audit_log
CREATE TRIGGER IF NOT EXISTS trg_audit_orders_insert
AFTER INSERT ON orders
BEGIN
    INSERT INTO audit_log (table_name, action, record_id)
    VALUES ('orders', 'INSERT', NEW.order_id);
END;

-- 2. Автоматическое обновление остатков на складе при добавлении товара в заказ
-- (Когда мы добавляем запись в order_items, количество на складе уменьшается)
CREATE TRIGGER IF NOT EXISTS trg_update_stock_after_order
AFTER INSERT ON order_items
BEGIN
    UPDATE stock_items 
    SET quantity = quantity - NEW.quantity 
    WHERE stock_item_id = NEW.stock_item_id;
END;

-- 3. Запрет удаления пользователя, у которого есть заказы
CREATE TRIGGER IF NOT EXISTS trg_prevent_user_delete
BEFORE DELETE ON users
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM orders WHERE user_id = OLD.user_id) > 0
        THEN RAISE(ABORT, 'Нельзя удалить пользователя, у которого есть заказы!')
    END;
END;