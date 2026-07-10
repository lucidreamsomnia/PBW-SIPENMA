-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 10, 2026 at 12:07 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sipenma`
--

-- --------------------------------------------------------

--
-- Table structure for table `audit_log`
--

CREATE TABLE `audit_log` (
  `id_log` bigint(20) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `aktivitas` varchar(255) NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `device` varchar(150) DEFAULT NULL,
  `waktu` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `detail_nilai`
--

CREATE TABLE `detail_nilai` (
  `id_detail` int(11) NOT NULL,
  `id_nilai` int(11) NOT NULL,
  `id_komponen` int(11) NOT NULL,
  `nilai` decimal(5,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dosen`
--

CREATE TABLE `dosen` (
  `id_dosen` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `nidn` varchar(20) NOT NULL,
  `nama_dosen` varchar(100) NOT NULL,
  `gelar_depan` varchar(30) DEFAULT NULL,
  `gelar_belakang` varchar(30) DEFAULT NULL,
  `jabatan` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `no_hp` varchar(20) DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `status_dosen` enum('Aktif','Tidak Aktif') DEFAULT 'Aktif',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Triggers `dosen`
--
DELIMITER $$
CREATE TRIGGER `trg_dosen_after_insert_audit` AFTER INSERT ON `dosen` FOR EACH ROW BEGIN
    INSERT INTO audit_log(id_user,aktivitas)
    VALUES(NEW.id_user, CONCAT('Data dosen ditambahkan: ', NEW.nama_dosen));
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `grade`
--

CREATE TABLE `grade` (
  `id_grade` int(11) NOT NULL,
  `nama_grade` varchar(5) DEFAULT NULL,
  `nilai_min` decimal(5,2) NOT NULL,
  `nilai_max` decimal(5,2) NOT NULL,
  `bobot` decimal(3,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `kelas`
--

CREATE TABLE `kelas` (
  `id_kelas` int(11) NOT NULL,
  `id_mk` int(11) NOT NULL,
  `id_dosen` int(11) NOT NULL,
  `id_tahun` int(11) NOT NULL,
  `nama_kelas` varchar(20) DEFAULT NULL,
  `ruangan` varchar(30) DEFAULT NULL,
  `hari` enum('Senin','Selasa','Rabu','Kamis','Jumat','Sabtu') DEFAULT NULL,
  `jam_mulai` time DEFAULT NULL,
  `jam_selesai` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `komponen_nilai`
--

CREATE TABLE `komponen_nilai` (
  `id_komponen` int(11) NOT NULL,
  `nama_komponen` varchar(50) NOT NULL,
  `bobot` decimal(5,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `krs`
--

CREATE TABLE `krs` (
  `id_krs` int(11) NOT NULL,
  `id_mahasiswa` int(11) NOT NULL,
  `id_kelas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `mahasiswa`
--

CREATE TABLE `mahasiswa` (
  `id_mahasiswa` int(11) NOT NULL,
  `nim` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `id_prodi` int(11) NOT NULL,
  `angkatan` year(4) NOT NULL,
  `jenis_kelamin` enum('L','P') NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `no_hp` varchar(20) DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `status_mahasiswa` enum('Aktif','Cuti','Lulus','DO') DEFAULT 'Aktif',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Triggers `mahasiswa`
--
DELIMITER $$
CREATE TRIGGER `trg_mahasiswa_after_insert_audit` AFTER INSERT ON `mahasiswa` FOR EACH ROW BEGIN
    INSERT INTO audit_log(id_user,aktivitas)
    VALUES(NULL, CONCAT('Mahasiswa ditambahkan: ', NEW.nim,' - ',NEW.nama));
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `mata_kuliah`
--

CREATE TABLE `mata_kuliah` (
  `id_mk` int(11) NOT NULL,
  `kode_mk` varchar(20) NOT NULL,
  `nama_mk` varchar(120) NOT NULL,
  `sks` tinyint(4) NOT NULL,
  `semester_rekomendasi` tinyint(4) DEFAULT NULL,
  `status_mk` enum('Aktif','Nonaktif') DEFAULT 'Aktif',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `nilai`
--

CREATE TABLE `nilai` (
  `id_nilai` int(11) NOT NULL,
  `id_krs` int(11) NOT NULL,
  `id_grade` int(11) DEFAULT NULL,
  `nilai_akhir` decimal(5,2) DEFAULT NULL,
  `status_publish` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Triggers `nilai`
--
DELIMITER $$
CREATE TRIGGER `trg_nilai_after_update_audit` AFTER UPDATE ON `nilai` FOR EACH ROW BEGIN
    INSERT INTO audit_log(id_user,aktivitas)
    VALUES(NULL,
        CONCAT(
            'Nilai diperbarui. ID Nilai: ',
            NEW.id_nilai,
            ', Nilai Akhir: ',
            IFNULL(NEW.nilai_akhir,0)
        )
    );
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_nilai_before_insert` BEFORE INSERT ON `nilai` FOR EACH ROW BEGIN
    IF NEW.nilai_akhir IS NOT NULL THEN
        SET NEW.nilai_akhir = ROUND(NEW.nilai_akhir,2);
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_nilai_before_update` BEFORE UPDATE ON `nilai` FOR EACH ROW BEGIN
    IF NEW.nilai_akhir IS NOT NULL THEN
        SET NEW.nilai_akhir = ROUND(NEW.nilai_akhir,2);
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `notifikasi`
--

CREATE TABLE `notifikasi` (
  `id_notifikasi` int(11) NOT NULL,
  `id_mahasiswa` int(11) NOT NULL,
  `judul` varchar(100) NOT NULL,
  `pesan` text NOT NULL,
  `dibaca` tinyint(1) DEFAULT 0,
  `waktu_kirim` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Triggers `notifikasi`
--
DELIMITER $$
CREATE TRIGGER `trg_notifikasi_after_insert` AFTER INSERT ON `notifikasi` FOR EACH ROW BEGIN
    INSERT INTO audit_log(id_user,aktivitas)
    VALUES(NULL,
        CONCAT(
            'Notifikasi dikirim ke Mahasiswa ID ',
            NEW.id_mahasiswa
        )
    );
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `program_studi`
--

CREATE TABLE `program_studi` (
  `id_prodi` int(11) NOT NULL,
  `nama_prodi` varchar(100) NOT NULL,
  `fakultas` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `id_role` int(11) NOT NULL,
  `nama_role` varchar(30) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tahun_ajaran`
--

CREATE TABLE `tahun_ajaran` (
  `id_tahun` int(11) NOT NULL,
  `tahun_mulai` year(4) NOT NULL,
  `tahun_selesai` year(4) NOT NULL,
  `semester` enum('Ganjil','Genap') NOT NULL,
  `aktif` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id_user` int(11) NOT NULL,
  `id_role` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `refresh_token` varchar(255) DEFAULT NULL,
  `status_aktif` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Triggers `user`
--
DELIMITER $$
CREATE TRIGGER `trg_user_after_insert_audit` AFTER INSERT ON `user` FOR EACH ROW BEGIN
    INSERT INTO audit_log(id_user,aktivitas)
    VALUES(NEW.id_user, CONCAT('User dibuat: ', NEW.username));
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_dashboard`
-- (See below for the actual view)
--
CREATE TABLE `v_dashboard` (
`total_mahasiswa` bigint(21)
,`total_dosen` bigint(21)
,`total_mata_kuliah` bigint(21)
,`total_kelas` bigint(21)
,`rata_rata_nilai` decimal(6,2)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_grade_distribution`
-- (See below for the actual view)
--
CREATE TABLE `v_grade_distribution` (
`nama_grade` varchar(5)
,`jumlah_mahasiswa` bigint(21)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_mahasiswa_kelas`
-- (See below for the actual view)
--
CREATE TABLE `v_mahasiswa_kelas` (
`nim` varchar(20)
,`nama` varchar(100)
,`kode_mk` varchar(20)
,`nama_mk` varchar(120)
,`nama_kelas` varchar(20)
,`nama_dosen` varchar(100)
,`tahun_mulai` year(4)
,`tahun_selesai` year(4)
,`semester` enum('Ganjil','Genap')
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_nilai_per_matakuliah`
-- (See below for the actual view)
--
CREATE TABLE `v_nilai_per_matakuliah` (
`id_mk` int(11)
,`kode_mk` varchar(20)
,`nama_mk` varchar(120)
,`rata_rata_nilai` decimal(6,2)
,`jumlah_data` bigint(21)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_rekap_nilai`
-- (See below for the actual view)
--
CREATE TABLE `v_rekap_nilai` (
`id_nilai` int(11)
,`nim` varchar(20)
,`nama_mahasiswa` varchar(100)
,`kode_mk` varchar(20)
,`nama_mk` varchar(120)
,`nilai_akhir` decimal(5,2)
,`grade` varchar(5)
,`status_publish` tinyint(1)
,`tahun_mulai` year(4)
,`tahun_selesai` year(4)
,`semester` enum('Ganjil','Genap')
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_statistik_dosen`
-- (See below for the actual view)
--
CREATE TABLE `v_statistik_dosen` (
`id_dosen` int(11)
,`nama_dosen` varchar(100)
,`jumlah_kelas_diampu` bigint(21)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_statistik_prodi`
-- (See below for the actual view)
--
CREATE TABLE `v_statistik_prodi` (
`id_prodi` int(11)
,`nama_prodi` varchar(100)
,`jumlah_mahasiswa` bigint(21)
);

-- --------------------------------------------------------

--
-- Structure for view `v_dashboard`
--
DROP TABLE IF EXISTS `v_dashboard`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_dashboard`  AS SELECT (select count(0) from `mahasiswa`) AS `total_mahasiswa`, (select count(0) from `dosen`) AS `total_dosen`, (select count(0) from `mata_kuliah`) AS `total_mata_kuliah`, (select count(0) from `kelas`) AS `total_kelas`, (select round(avg(`nilai`.`nilai_akhir`),2) from `nilai`) AS `rata_rata_nilai` ;

-- --------------------------------------------------------

--
-- Structure for view `v_grade_distribution`
--
DROP TABLE IF EXISTS `v_grade_distribution`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_grade_distribution`  AS SELECT `g`.`nama_grade` AS `nama_grade`, count(`n`.`id_nilai`) AS `jumlah_mahasiswa` FROM (`grade` `g` left join `nilai` `n` on(`g`.`id_grade` = `n`.`id_grade`)) GROUP BY `g`.`id_grade`, `g`.`nama_grade` ORDER BY `g`.`nilai_min` DESC ;

-- --------------------------------------------------------

--
-- Structure for view `v_mahasiswa_kelas`
--
DROP TABLE IF EXISTS `v_mahasiswa_kelas`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_mahasiswa_kelas`  AS SELECT `m`.`nim` AS `nim`, `m`.`nama` AS `nama`, `mk`.`kode_mk` AS `kode_mk`, `mk`.`nama_mk` AS `nama_mk`, `k`.`nama_kelas` AS `nama_kelas`, `d`.`nama_dosen` AS `nama_dosen`, `ta`.`tahun_mulai` AS `tahun_mulai`, `ta`.`tahun_selesai` AS `tahun_selesai`, `ta`.`semester` AS `semester` FROM (((((`krs` `kr` join `mahasiswa` `m` on(`kr`.`id_mahasiswa` = `m`.`id_mahasiswa`)) join `kelas` `k` on(`kr`.`id_kelas` = `k`.`id_kelas`)) join `mata_kuliah` `mk` on(`k`.`id_mk` = `mk`.`id_mk`)) join `dosen` `d` on(`k`.`id_dosen` = `d`.`id_dosen`)) join `tahun_ajaran` `ta` on(`k`.`id_tahun` = `ta`.`id_tahun`)) ;

-- --------------------------------------------------------

--
-- Structure for view `v_nilai_per_matakuliah`
--
DROP TABLE IF EXISTS `v_nilai_per_matakuliah`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_nilai_per_matakuliah`  AS SELECT `mk`.`id_mk` AS `id_mk`, `mk`.`kode_mk` AS `kode_mk`, `mk`.`nama_mk` AS `nama_mk`, round(avg(`n`.`nilai_akhir`),2) AS `rata_rata_nilai`, count(`n`.`id_nilai`) AS `jumlah_data` FROM (((`mata_kuliah` `mk` left join `kelas` `k` on(`mk`.`id_mk` = `k`.`id_mk`)) left join `krs` `kr` on(`k`.`id_kelas` = `kr`.`id_kelas`)) left join `nilai` `n` on(`kr`.`id_krs` = `n`.`id_krs`)) GROUP BY `mk`.`id_mk`, `mk`.`kode_mk`, `mk`.`nama_mk` ;

-- --------------------------------------------------------

--
-- Structure for view `v_rekap_nilai`
--
DROP TABLE IF EXISTS `v_rekap_nilai`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_rekap_nilai`  AS SELECT `n`.`id_nilai` AS `id_nilai`, `m`.`nim` AS `nim`, `m`.`nama` AS `nama_mahasiswa`, `mk`.`kode_mk` AS `kode_mk`, `mk`.`nama_mk` AS `nama_mk`, `n`.`nilai_akhir` AS `nilai_akhir`, `g`.`nama_grade` AS `grade`, `n`.`status_publish` AS `status_publish`, `ta`.`tahun_mulai` AS `tahun_mulai`, `ta`.`tahun_selesai` AS `tahun_selesai`, `ta`.`semester` AS `semester` FROM ((((((`nilai` `n` join `grade` `g` on(`n`.`id_grade` = `g`.`id_grade`)) join `krs` `k` on(`n`.`id_krs` = `k`.`id_krs`)) join `mahasiswa` `m` on(`k`.`id_mahasiswa` = `m`.`id_mahasiswa`)) join `kelas` `ks` on(`k`.`id_kelas` = `ks`.`id_kelas`)) join `mata_kuliah` `mk` on(`ks`.`id_mk` = `mk`.`id_mk`)) join `tahun_ajaran` `ta` on(`ks`.`id_tahun` = `ta`.`id_tahun`)) ;

-- --------------------------------------------------------

--
-- Structure for view `v_statistik_dosen`
--
DROP TABLE IF EXISTS `v_statistik_dosen`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_statistik_dosen`  AS SELECT `d`.`id_dosen` AS `id_dosen`, `d`.`nama_dosen` AS `nama_dosen`, count(`k`.`id_kelas`) AS `jumlah_kelas_diampu` FROM (`dosen` `d` left join `kelas` `k` on(`d`.`id_dosen` = `k`.`id_dosen`)) GROUP BY `d`.`id_dosen`, `d`.`nama_dosen` ;

-- --------------------------------------------------------

--
-- Structure for view `v_statistik_prodi`
--
DROP TABLE IF EXISTS `v_statistik_prodi`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_statistik_prodi`  AS SELECT `ps`.`id_prodi` AS `id_prodi`, `ps`.`nama_prodi` AS `nama_prodi`, count(`m`.`id_mahasiswa`) AS `jumlah_mahasiswa` FROM (`program_studi` `ps` left join `mahasiswa` `m` on(`ps`.`id_prodi` = `m`.`id_prodi`)) GROUP BY `ps`.`id_prodi`, `ps`.`nama_prodi` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `audit_log`
--
ALTER TABLE `audit_log`
  ADD PRIMARY KEY (`id_log`),
  ADD KEY `fk_audit_user` (`id_user`);

--
-- Indexes for table `detail_nilai`
--
ALTER TABLE `detail_nilai`
  ADD PRIMARY KEY (`id_detail`),
  ADD UNIQUE KEY `id_nilai` (`id_nilai`,`id_komponen`),
  ADD KEY `fk_detail_komponen` (`id_komponen`);

--
-- Indexes for table `dosen`
--
ALTER TABLE `dosen`
  ADD PRIMARY KEY (`id_dosen`),
  ADD UNIQUE KEY `id_user` (`id_user`),
  ADD UNIQUE KEY `nidn` (`nidn`);

--
-- Indexes for table `grade`
--
ALTER TABLE `grade`
  ADD PRIMARY KEY (`id_grade`),
  ADD UNIQUE KEY `nama_grade` (`nama_grade`);

--
-- Indexes for table `kelas`
--
ALTER TABLE `kelas`
  ADD PRIMARY KEY (`id_kelas`),
  ADD KEY `idx_dosen` (`id_dosen`),
  ADD KEY `fk_kelas_mk` (`id_mk`),
  ADD KEY `fk_kelas_tahun` (`id_tahun`);

--
-- Indexes for table `komponen_nilai`
--
ALTER TABLE `komponen_nilai`
  ADD PRIMARY KEY (`id_komponen`),
  ADD UNIQUE KEY `nama_komponen` (`nama_komponen`);

--
-- Indexes for table `krs`
--
ALTER TABLE `krs`
  ADD PRIMARY KEY (`id_krs`),
  ADD UNIQUE KEY `id_mahasiswa` (`id_mahasiswa`,`id_kelas`),
  ADD KEY `fk_krs_kelas` (`id_kelas`);

--
-- Indexes for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD PRIMARY KEY (`id_mahasiswa`),
  ADD UNIQUE KEY `nim` (`nim`),
  ADD KEY `idx_nim` (`nim`),
  ADD KEY `fk_mhs_prodi` (`id_prodi`);

--
-- Indexes for table `mata_kuliah`
--
ALTER TABLE `mata_kuliah`
  ADD PRIMARY KEY (`id_mk`),
  ADD UNIQUE KEY `kode_mk` (`kode_mk`);

--
-- Indexes for table `nilai`
--
ALTER TABLE `nilai`
  ADD PRIMARY KEY (`id_nilai`),
  ADD UNIQUE KEY `id_krs` (`id_krs`),
  ADD KEY `fk_nilai_grade` (`id_grade`);

--
-- Indexes for table `notifikasi`
--
ALTER TABLE `notifikasi`
  ADD PRIMARY KEY (`id_notifikasi`),
  ADD KEY `fk_notif_mhs` (`id_mahasiswa`);

--
-- Indexes for table `program_studi`
--
ALTER TABLE `program_studi`
  ADD PRIMARY KEY (`id_prodi`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`id_role`),
  ADD UNIQUE KEY `nama_role` (`nama_role`);

--
-- Indexes for table `tahun_ajaran`
--
ALTER TABLE `tahun_ajaran`
  ADD PRIMARY KEY (`id_tahun`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `fk_user_role` (`id_role`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `audit_log`
--
ALTER TABLE `audit_log`
  MODIFY `id_log` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `detail_nilai`
--
ALTER TABLE `detail_nilai`
  MODIFY `id_detail` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `dosen`
--
ALTER TABLE `dosen`
  MODIFY `id_dosen` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `grade`
--
ALTER TABLE `grade`
  MODIFY `id_grade` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `kelas`
--
ALTER TABLE `kelas`
  MODIFY `id_kelas` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `komponen_nilai`
--
ALTER TABLE `komponen_nilai`
  MODIFY `id_komponen` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `krs`
--
ALTER TABLE `krs`
  MODIFY `id_krs` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  MODIFY `id_mahasiswa` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `mata_kuliah`
--
ALTER TABLE `mata_kuliah`
  MODIFY `id_mk` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `nilai`
--
ALTER TABLE `nilai`
  MODIFY `id_nilai` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notifikasi`
--
ALTER TABLE `notifikasi`
  MODIFY `id_notifikasi` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_studi`
--
ALTER TABLE `program_studi`
  MODIFY `id_prodi` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `id_role` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tahun_ajaran`
--
ALTER TABLE `tahun_ajaran`
  MODIFY `id_tahun` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `audit_log`
--
ALTER TABLE `audit_log`
  ADD CONSTRAINT `fk_audit_user` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `detail_nilai`
--
ALTER TABLE `detail_nilai`
  ADD CONSTRAINT `fk_detail_komponen` FOREIGN KEY (`id_komponen`) REFERENCES `komponen_nilai` (`id_komponen`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_detail_nilai` FOREIGN KEY (`id_nilai`) REFERENCES `nilai` (`id_nilai`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `dosen`
--
ALTER TABLE `dosen`
  ADD CONSTRAINT `fk_dosen_user` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`) ON UPDATE CASCADE;

--
-- Constraints for table `kelas`
--
ALTER TABLE `kelas`
  ADD CONSTRAINT `fk_kelas_dosen` FOREIGN KEY (`id_dosen`) REFERENCES `dosen` (`id_dosen`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_kelas_mk` FOREIGN KEY (`id_mk`) REFERENCES `mata_kuliah` (`id_mk`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_kelas_tahun` FOREIGN KEY (`id_tahun`) REFERENCES `tahun_ajaran` (`id_tahun`) ON UPDATE CASCADE;

--
-- Constraints for table `krs`
--
ALTER TABLE `krs`
  ADD CONSTRAINT `fk_krs_kelas` FOREIGN KEY (`id_kelas`) REFERENCES `kelas` (`id_kelas`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_krs_mhs` FOREIGN KEY (`id_mahasiswa`) REFERENCES `mahasiswa` (`id_mahasiswa`) ON UPDATE CASCADE;

--
-- Constraints for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD CONSTRAINT `fk_mhs_prodi` FOREIGN KEY (`id_prodi`) REFERENCES `program_studi` (`id_prodi`) ON UPDATE CASCADE;

--
-- Constraints for table `nilai`
--
ALTER TABLE `nilai`
  ADD CONSTRAINT `fk_nilai_grade` FOREIGN KEY (`id_grade`) REFERENCES `grade` (`id_grade`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_nilai_krs` FOREIGN KEY (`id_krs`) REFERENCES `krs` (`id_krs`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `notifikasi`
--
ALTER TABLE `notifikasi`
  ADD CONSTRAINT `fk_notif_mhs` FOREIGN KEY (`id_mahasiswa`) REFERENCES `mahasiswa` (`id_mahasiswa`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `fk_user_role` FOREIGN KEY (`id_role`) REFERENCES `role` (`id_role`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
