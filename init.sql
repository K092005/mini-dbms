CREATE DATABASE IF NOT EXISTS bloodDonation;
USE bloodDonation;

CREATE TABLE IF NOT EXISTS doctor (
    doctor_id INT NOT NULL,
    doctor_name VARCHAR(20),
    doctor_phone BIGINT,
    PRIMARY KEY(doctor_id)
);

CREATE TABLE IF NOT EXISTS donor (
    donor_id INT NOT NULL,
    donor_name VARCHAR(20),
    phone_no BIGINT,
    DOB DATE,
    gender CHAR(1),
    address VARCHAR(30),
    weight INT,
    blood_pressure INT,
    iron_content INT,
    doctor_id INT,
    PRIMARY KEY(donor_id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id)
);

CREATE TABLE IF NOT EXISTS blood_bank (
    blood_bank_id INT NOT NULL,
    blood_bank_name VARCHAR(50),
    baddress VARCHAR(30),
    PRIMARY KEY(blood_bank_id)
);

CREATE TABLE IF NOT EXISTS blood (
    blood_type VARCHAR(20),
    donor_id INT,
    blood_bank_id INT,
    PRIMARY KEY(donor_id),
    FOREIGN KEY (donor_id) REFERENCES donor(donor_id),
    FOREIGN KEY (blood_bank_id) REFERENCES blood_bank(blood_bank_id)
);

CREATE TABLE IF NOT EXISTS patient (
    patient_id INT NOT NULL,
    patient_name VARCHAR(20),
    p_phno BIGINT,
    h_add VARCHAR(50),
    p_add VARCHAR(50),
    PRIMARY KEY(patient_id)
);

CREATE TABLE IF NOT EXISTS blood_delivery (
    blood_bank_id INT,
    patient_id INT,
    FOREIGN KEY(blood_bank_id) REFERENCES blood_bank(blood_bank_id),
    FOREIGN KEY(patient_id) REFERENCES patient(patient_id)
);

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS main(IN no INT, IN value VARCHAR(20))
BEGIN
    SELECT blood_type, COUNT(blood_type) AS count1
    FROM blood b1
    WHERE blood_type = value
      AND EXISTS (
          SELECT blood_bank_id FROM blood_bank b2
          WHERE blood_bank_id = no AND b1.blood_bank_id = b2.blood_bank_id
      )
    GROUP BY blood_type;
END //
DELIMITER ;
DELIMITER //

CREATE TRIGGER check_donor_eligibility
BEFORE INSERT ON donor
FOR EACH ROW
BEGIN
    IF NEW.weight < 50 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Donor weight is below minimum (50kg)';
    END IF;

    IF NEW.blood_pressure < 90 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Blood pressure too low for donation';
    END IF;

    IF NEW.iron_content < 12 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Iron content too low for donation';
    END IF;
END //

DELIMITER ;

