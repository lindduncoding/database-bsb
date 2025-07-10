-- Autogenerate Nomor Rekening
CREATE TRIGGER autogenerate_rekening -- nama trigger adalah autogenerate_rekening
BEFORE INSERT ON nasabah
FOR EACH ROW
BEGIN
    DECLARE new_seq INT;
    DECLARE today_str CHAR(8);

    -- Dapatkan Sequence
    INSERT INTO nasabah_seq VALUES (NULL);
    SET new_seq = LAST_INSERT_ID();

    -- Auto generate berdasarkan datetime dan prefix NSB
    SET today_str = DATE_FORMAT(CURDATE(), '%Y%m%d');
    SET NEW.no_rekening = CONCAT('NSB', today_str, LPAD(new_seq, 4, '0'));
END

-- Autogenerate Nomor Pembeli
CREATE TRIGGER autogenerate_no_pembeli
BEFORE INSERT ON pembeli
FOR EACH ROW
BEGIN
    DECLARE new_seq INT;
    DECLARE today_str CHAR(8);

    -- Dapatkan Sequence
    INSERT INTO pembeli_seq VALUES (NULL);
    SET new_seq = LAST_INSERT_ID();

    -- Auto generate berdasarkan datetime dan prefix NSB
    SET today_str = DATE_FORMAT(CURDATE(), '%Y%m%d');
    SET NEW.no_pembeli = CONCAT('NPB', today_str, LPAD(new_seq, 4, '0'));
END;

-- Autogenerate Nomor Invoice Pembelian
CREATE TRIGGER autogenerate_invoice
BEFORE INSERT ON pembelian 
FOR EACH ROW
BEGIN
    DECLARE new_seq INT;
    DECLARE today_str CHAR(8);

    INSERT INTO invoice_seq (date_key) VALUES (CURDATE());
    SET new_seq = LAST_INSERT_ID();

    SET today_str = DATE_FORMAT(CURDATE(), '%Y%m%d');
    SET NEW.no_invoice = CONCAT('INV', today_str, LPAD(new_seq, 4, '0'));
END;

CREATE TRIGGER autogenerate_invoice_penjualan
BEFORE INSERT ON penjualan
FOR EACH ROW
BEGIN
    DECLARE new_seq INT;
    DECLARE today_str CHAR(8);

    INSERT INTO invoice_seq (date_key) VALUES (CURDATE());
    SET new_seq = LAST_INSERT_ID();

    SET today_str = DATE_FORMAT(CURDATE(), '%Y%m%d');
    SET NEW.no_invoice = CONCAT('INV', today_str, LPAD(new_seq, 4, '0'));
END;