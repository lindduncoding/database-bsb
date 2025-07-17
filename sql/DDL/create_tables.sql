-- sampah.nasabah definition

CREATE TABLE `nasabah` (
  `nasabah_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) NOT NULL,
  `no_rekening` varchar(16) NOT NULL,
  PRIMARY KEY (`nasabah_id`),
  UNIQUE KEY `nasabah_unique` (`nama`),
  UNIQUE KEY `nasabah_unique_1` (`no_rekening`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- sampah.pembeli definition

CREATE TABLE `pembeli` (
  `pembeli_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) NOT NULL,
  `no_pembeli` varchar(16) NOT NULL,
  PRIMARY KEY (`pembeli_id`),
  UNIQUE KEY `pembeli_unique` (`nama`),
  UNIQUE KEY `pembeli_unique_1` (`no_pembeli`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- sampah.harga_satuan definition

CREATE TABLE `harga_satuan` (
  `tipe_sampah` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `nama_sampah` varchar(100) NOT NULL,
  `satuan_beli` float NOT NULL DEFAULT 0,
  `satuan_jual` float NOT NULL DEFAULT 0,
  PRIMARY KEY (`tipe_sampah`),
  UNIQUE KEY `harga_satuan_unique` (`nama_sampah`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- sampah.sampah definition

CREATE TABLE `sampah` (
  `sampah_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `berat` float NOT NULL DEFAULT 0,
  `tipe_sampah` bigint(20) unsigned NOT NULL,
  `is_sold` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`sampah_id`),
  KEY `sampah_harga_satuan_FK` (`tipe_sampah`),
  CONSTRAINT `sampah_harga_satuan_FK` FOREIGN KEY (`tipe_sampah`) REFERENCES `harga_satuan` (`tipe_sampah`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- sampah.pembelian definition

CREATE TABLE `pembelian` (
  `beli_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `nasabah_id` bigint(20) unsigned NOT NULL,
  `sampah_id` bigint(20) unsigned NOT NULL,
  `no_invoice` varchar(16) NOT NULL,
  `harga_beli` float NOT NULL DEFAULT 0,
  `tanggal_beli` datetime NOT NULL,
  PRIMARY KEY (`beli_id`),
  UNIQUE KEY `pembelian_unique` (`no_invoice`),
  KEY `pembelian_sampah_FK` (`sampah_id`),
  KEY `pembelian_nasabah_FK` (`nasabah_id`),
  CONSTRAINT `pembelian_nasabah_FK` FOREIGN KEY (`nasabah_id`) REFERENCES `nasabah` (`nasabah_id`),
  CONSTRAINT `pembelian_sampah_FK` FOREIGN KEY (`sampah_id`) REFERENCES `sampah` (`sampah_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- sampah.penjualan definition

CREATE TABLE `penjualan` (
  `jual_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `pembeli_id` bigint(20) unsigned NOT NULL,
  `sampah_id` bigint(20) unsigned NOT NULL,
  `no_invoice` varchar(16) NOT NULL,
  `harga_jual` float NOT NULL,
  `tanggal_jual` datetime NOT NULL,
  PRIMARY KEY (`jual_id`),
  UNIQUE KEY `penjualan_unique` (`no_invoice`),
  KEY `penjualan_pembeli_FK` (`pembeli_id`),
  KEY `penjualan_sampah_FK` (`sampah_id`),
  CONSTRAINT `penjualan_pembeli_FK` FOREIGN KEY (`pembeli_id`) REFERENCES `pembeli` (`pembeli_id`),
  CONSTRAINT `penjualan_sampah_FK` FOREIGN KEY (`sampah_id`) REFERENCES `sampah` (`sampah_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- tabel sequence untuk memudahkan generation no rekening dan no pembeli

CREATE TABLE invoice_seq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_key DATE NOT NULL
);

CREATE TABLE nasabah_seq (
    seq INT AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE pembeli_seq (
    seq INT AUTO_INCREMENT PRIMARY KEY
);
