-- Create Authentication database
CREATE DATABASE IF NOT EXISTS `plantdb3`;
USE `plantdb3`;

-- Create Users table
CREATE TABLE IF NOT EXISTS Users (
    Username VARCHAR(50) PRIMARY KEY,
    Password VARCHAR(255),
    Role VARCHAR(10)
);

-- Create Plant_Species table
CREATE TABLE IF NOT EXISTS Plant_Species (
    Species_ID INT AUTO_INCREMENT PRIMARY KEY,
    Common_Name VARCHAR(100),
    Scientific_Name VARCHAR(100),
    Family VARCHAR(100)
);

-- Insert data into Plant_Species table
-- INSERT IGNORE INTO Plant_Species (Common_Name, Scientific_Name, Family) VALUES
--    ('Red Rose', 'Rosa rubra', 'Rosaceae'),
--    ('Sunflower', 'Helianthus annuus', 'Asteraceae'),
--    ('Tulip', 'Tulipa gesneriana', 'Liliaceae');
    
-- Create Genome table
-- Create Genome table
CREATE TABLE IF NOT EXISTS Genome (
    Genome_ID INT AUTO_INCREMENT PRIMARY KEY,
    Species_ID INT,
    Genome_Size DECIMAL(10, 2),
    Chromosome_Count INT,
    FOREIGN KEY (Species_ID) REFERENCES Plant_Species(Species_ID)
);

-- Insert data into Genome table
-- INSERT IGNORE INTO Genome (Species_ID, Genome_Size, Chromosome_Count) VALUES
--     (1, 120.5, 12),
--     (2, 90.2, 8),
--     (3, 75.8, 10);

-- Create Chromosome table
CREATE TABLE IF NOT EXISTS Chromosome (
    Chromosome_ID INT AUTO_INCREMENT PRIMARY KEY,
    Genome_ID INT,
    Chromosome_Number INT,
    Length DECIMAL(10, 2),
    Genes_Count INT,
    FOREIGN KEY (Genome_ID) REFERENCES Genome(Genome_ID)
);

-- Insert data into Chromosome table
-- INSERT IGNORE INTO Chromosome (Genome_ID, Chromosome_Number, Length, Genes_Count) VALUES
--     (1, 1, 20.3, 150),
--     (1, 2, 18.5, 120),
--     (2, 1, 15.7, 100),
--     (2, 2, 14.2, 80),
--     (3, 1, 12.8, 110),
--     (3, 2, 11.5, 90);


-- Create Gene table
CREATE TABLE IF NOT EXISTS Gene (
    Gene_ID INT AUTO_INCREMENT PRIMARY KEY,
    Chromosome_ID INT,
    Gene_Name VARCHAR(100),
    Gene_Description TEXT,
    Start_Position INT,
    End_Position INT,
    Strand ENUM('+', '-'),
    FOREIGN KEY (Chromosome_ID) REFERENCES Chromosome(Chromosome_ID)
);

-- Insert data into Gene table
-- INSERT IGNORE INTO Gene (Chromosome_ID, Gene_Name, Gene_Description, Start_Position, End_Position, Strand) VALUES
--     (1, 'RUBRA_gene1', 'Red Rose Gene 1', 100, 300, '+'),
--     (2, 'RUBRA_gene2', 'Red Rose Gene 2', 200, 400, '-'),
--     (3, 'ANNUUS_gene1', 'Sunflower Gene 1', 50, 250, '+'),
--     (4, 'ANNUUS_gene2', 'Sunflower Gene 2', 150, 350, '-'),
--     (5, 'GESNERIANA_gene1', 'Tulip Gene 1', 80, 280, '+'),
--     (6, 'GESNERIANA_gene2', 'Tulip Gene 2', 180, 380, '-');

-- Create Allele table
CREATE TABLE IF NOT EXISTS Allele (
    Allele_ID INT AUTO_INCREMENT PRIMARY KEY,
    Gene_ID INT,
    Allele_Name VARCHAR(100),
    Allele_Type VARCHAR(100),
    Mutation_Type VARCHAR(100),
    FOREIGN KEY (Gene_ID) REFERENCES Gene(Gene_ID)
);

-- Insert data into Allele table
-- INSERT IGNORE INTO Allele (Gene_ID, Allele_Name, Allele_Type, Mutation_Type) VALUES
--     (1, 'RUBRA_allele1', 'TypeA', 'MutationA'),
--     (2, 'RUBRA_allele2', 'TypeB', 'MutationB'),
--     (3, 'ANNUUS_allele1', 'TypeC', 'MutationC'),
--     (4, 'ANNUUS_allele2', 'TypeD', 'MutationD'),
--     (5, 'GESNERIANA_allele1', 'TypeE', 'MutationE'),
--     (6, 'GESNERIANA_allele2', 'TypeF', 'MutationF');

-- Create DNA_Sequence table
CREATE TABLE IF NOT EXISTS DNA_Sequence (
    Sequence_ID INT AUTO_INCREMENT PRIMARY KEY,
    Gene_ID INT,
    Sequence_Data TEXT,
    Sequence_Length INT,
    FOREIGN KEY (Gene_ID) REFERENCES Gene(Gene_ID)
);

-- Insert data into DNA_Sequence table
-- INSERT IGNORE INTO DNA_Sequence (Gene_ID, Sequence_Data, Sequence_Length) VALUES
--     (1, 'ATCGATCGATCG', 12),
--     (2, 'GCTAGCTAGCTA', 12),
--     (3, 'TATCTATCTATC', 12),
--     (4, 'CGATCGAtCGAT', 12),
--     (5, 'TAGCTAGCTAGC', 12),
--     (6, 'ATCATCATCATC', 12);

-- Create Genetic_Variation table
CREATE TABLE IF NOT EXISTS Genetic_Variation (
    Variation_ID INT AUTO_INCREMENT PRIMARY KEY,
    Allele_ID INT,
    Variation_Type VARCHAR(100),
    Variation_Description TEXT,
    Position INT,
    Reference_Sequence TEXT,
    Altered_Sequence TEXT,
    FOREIGN KEY (Allele_ID) REFERENCES Allele(Allele_ID)
);

-- Insert data into Genetic_Variation table
-- INSERT IGNORE INTO Genetic_Variation (Allele_ID, Variation_Type, Variation_Description, Position, Reference_Sequence, Altered_Sequence) VALUES
--     (1, 'SNP', 'Single Nucleotide Polymorphism', 150, 'G', 'A'),
--     (2, 'Insertion', 'Insertion Mutation', 300, 'C', 'CGT'),
--     (3, 'Deletion', 'Deletion Mutation', 80, 'ATG', 'A'),
--     (4, 'SNP', 'Single Nucleotide Polymorphism', 200, 'T', 'G'),
--     (5, 'Insertion', 'Insertion Mutation', 120, 'A', 'ATG'),
--     (6, 'Deletion', 'Deletion Mutation', 250, 'GA', 'G');

-- Create Genotype table
CREATE TABLE IF NOT EXISTS Genotype (
    Genotype_ID INT AUTO_INCREMENT PRIMARY KEY,
    Allele_1 INT,
    Allele_2 INT,
    FOREIGN KEY (Allele_1) REFERENCES Allele(Allele_ID),
    FOREIGN KEY (Allele_2) REFERENCES Allele(Allele_ID)
);

-- Insert data into Genotype table
-- INSERT IGNORE INTO Genotype (Allele_1, Allele_2) VALUES
--     (1, 2),
--     (3, 4),
--     (5, 6);

-- Create Protein table
CREATE TABLE IF NOT EXISTS Protein (
    Protein_ID INT AUTO_INCREMENT,
    Protein_Name VARCHAR(100),
    Protein_Description TEXT,
    Gene_ID INT,
    PRIMARY KEY (Protein_ID, Gene_ID),
    FOREIGN KEY (Gene_ID) REFERENCES Gene(Gene_ID)
);

-- Insert data into Protein table
-- INSERT IGNORE INTO Protein (Protein_ID, Protein_Name, Protein_Description, Gene_ID) VALUES
--     (1, 'Alpha-1', 'Alpha Protein Variant 1', 1),
--     (2, 'Beta-1', 'Beta Protein Variant 1', 2),
--     (3, 'Gamma-1', 'Gamma Protein Variant 1', 3),
--     (4, 'Delta-1', 'Delta Protein Variant 1', 4),
--     (5, 'Epsilon-1', 'Epsilon Protein Variant 1', 5),
--     (6, 'Zeta-1', 'Zeta Protein Variant 1', 6);





