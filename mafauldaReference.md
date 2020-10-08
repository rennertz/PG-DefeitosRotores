# [MAFAULDA](http://www02.smt.ufrj.br/~offshore/mfs/page_01.html#SEC1)

Machinery Fault Database \[Online\]

## 1. Database Description

### 1.1. Introduction

This database is composed of 1951 multivariate time-series acquired by sensors on a SpectraQuest's Machinery Fault Simulator (MFS) Alignment-Balance-Vibration (ABVT). The 1951 comprises six different simulated states: normal function, imbalance fault, horizontal and vertical misalignment faults and, inner and outer bearing faults. This section describes the database.

For more information please contact **Felipe M. L. Ribeiro** ([felipe.ribeiro@smt.ufrj.br](mailto:felipe.ribeiro@smt.ufrj.br)).

### 1.2. Experimental Bench Specifications

The used SpectraQuest Inc. Alignment/Balance Vibration Trainer (ABVT) Machinery Fault Simulator (MFS).

| Specifications     | Values      |
|--------------------|-------------|
| Motor              | 1/4 CV      |
| DC Frequency range | 700-3600 rpm|
| System weight      | 22 kg       |
| Axis diameter      | 16 mm       |
| Axis length        | 520 mm      |
| Rotor              | 15.24 cm    |
| Bearings distance  | 390 mm      |

| Specifications  | Values        |
|-----------------|---------------|
| Number of balls | 8             |
| Balls diameter  | 0.7145 cm     |
| Cage diameter   | 2.8519 cm     |
| FTF             | 0.375 CPM/rpm |
| BPFO            | 2.998 CPM/rpm |
| BPFI            | 5.002 CPM/rpm |
| BSF             | 1.871 CPM/rpm |

### 1.3. Data Acquisition System

* Three **Industrial IMI Sensors, Model 601A01** accelerometers on the radial, axial and tangencial directions:
  * **Sensibility**  
(±20%) 100 mV per g (10.2 mV per m/s2);
  * **Frequency range**  
(±3 dB) 16-600000 CPM (0.27-10.000 Hz);
  * **Measurement range**  
±50 g (±490 m/s2).

* One **IMI Sensors triaxial accelerometer, Model 604B31**, returning data over the radial, axial and tangencial directions:
  * **Sensibility**  
(±20%) 100 mV per g (10.2 mV per m/s2);
  * **Frequency range**  
(±3 dB) 30-300000 CPM (0.5-5.000 Hz);
  * **Measurement range**  
±50 g (±490 m/s2)

* **Monarch Instrument MT-190** analog tachometer

* **Shure SM81** microphone with frequency range of 20-20.000 Hz

* Two **National Instruments NI 9234** 4 channel analog acquisition modules, with sample rate of 51.2 kHz

### 1.4. Sequences

Each sequence was generated at a 50 kHz sampling rate during 5 s, totaling 250.000 samples. Below its a summary of each type of sequence:

| Normal                  | 49   |
|-------------------------|------|
| Horizontal misalignment | 197  |
| Vertical misalignment   | 301  |
| Imbalance               | 333  |
| **Underhang bearing**          |
| Cage fault              | 188  |
| Outer race              | 184  |
| Ball fault              | 186  |
| **Overhang bearing**           |
| Cage fault              | 188  |
| Outer race              | 188  |
| Ball fault              | 137  |
| Total                   | 1951 |

#### 1.4.1. Normal Sequences

There are 49 sequences without any fault, each with a fixed rotation speed within the range from 737 rpm to 3686 rpm with steps of approximately 60 rpm.

#### 1.4.2. Imbalance Faults

Simulated with load values within the range from 6 g to 35 g. For each load value below 30 g, the rotation frequency assumed in the same 49 values employed in the normal operation case. For loads equal to or above 30 g, however, the resulting vibration makes impracticable for the system to achieve rotation frequencies above 3300 rpm, limiting the number of distinct rotation frequencies. The table below presents the number of sequences per weight.

| Weight (g) | Measurements |
|------------|--------------|
| 6          | 49           |
| 10         | 48           |
| 15         | 48           |
| 20         | 49           |
| 25         | 47           |
| 30         | 47           |
| 35         | 45           |
| Total      | 333          |

#### 1.4.3. Horizontal Parallel Misalignment

This type of fault was induced into the MFS by shifting the motor shaft horizontally of 0.5 mm, 1.0 mm, 1.5 mm, and 2.0 mm. Using the same range for the rotation frequency as in the normal operation for each horizontal shift, the table below presents the number of sequences per degree of misalignment.

|Misalignment (mm) | Measurements |
|------------------|--------------|
| 0.50             | 50           |
| 1.00             | 49           |
| 1.50             | 49           |
| 2.00             | 49           |
| Total            | 197          |

#### 1.4.4. Vertical Parallel Misalignment

This type of fault was induced into the MFS by shifting the motor shaft horizontally of 0.51 mm, 0.63 mm, 1.27 mm, 1.40 mm, 17.8 mm and 1.90 mm. Using the same range for the rotation frequency as in the normal operation for each vertical shift, the table below presents the number of sequences per degree of misalignment.

|Misalignment (mm) | Measurements |
|------------------|--------------|
| 0.51             | 51           |
| 0.63             | 50           |
| 1.27             | 50           |
| 1.40             | 50           |
| 1.78             | 50           |
| 1.90             | 50           |
| Total            | 301          |

#### 1.4.5. Bearing Faults

As one of the most complex elements of the machine, the rolling bearings are the most susceptible elements to fault occurrence. The ABVT manufacturer provided three defective bearing, each one with a distinct defective element (outer track, rolling elements, and inner track), that were placed one at a time in two different positions in the MFS experimental stand: between the rotor and the motor (underhang position), or in the external position, having the rotor between the bearing and the motor (overhang position). Bearing faults are practically imperceptible when there is no imbalance. So, three masses of 6 g, 20 g, and 35 g were added to induce a detectable effect, with different rotation frequencies as before.

##### **Underhang**

The table below presents the underhang cases with *outer track* faults.

| Weight (g) | Measurements |
|------------|--------------|
| 0          | 49           |
| 6          | 48           |
| 20         | 49           |
| 35         | 42           |
| Total      | 188          |

The table below presents the underhang cases with *rolling elements* faults.

| Weight (g) | Measurements |
|------------|--------------|
| 0          | 49           |
| 6          | 49           |
| 20         | 49           |
| 35         | 37           |
| Total      | 184          |

The table below presents the underhang cases with *inner track* faults.

| Weight (g) | Measurements |
|------------|--------------|
| 0          | 50           |
| 6          | 49           |
| 20         | 49           |
| 35         | 38           |
| Total      | 186          |

The underhang has a total of **558** sequences.

##### **Overerhang**

The table below presents the overhang cases with *outer track* faults.

| Weight (g) | Measurements |
|------------|--------------|
| 0          | 49           |
| 6          | 49           |
| 20         | 49           |
| 35         | 41           |
| Total      | 188          |

The table below presents the overhang cases with *rolling elements* faults.

| Weight (g) | Measurements |
|------------|--------------|
| 0          | 49           |
| 6          | 49           |
| 20         | 49           |
| 35         | 41           |
| Total      | 188          |

The table below presents the overhang cases with *inner track* faults.

| Weight (g) | Measurements |
|------------|--------------|
| 0          | 49           |
| 6          | 43           |
| 20         | 25           |
| 35         | 20           |
| Total      | 137          |

The overhang sequences totaling **513**.

## 2. Machinery Fault Database \[Online\]

The following table contains links to entire parts of this database, joined in as a single package.

| Description | Tgz File | Size (GB) | Zip File | Size (GB)|
|-------------|----------|-----------|----------|----------|
| **All Data** | [Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/full.tgz) |13.0 | [Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/full.zip) | 13.0|
| **Normal (No fault)** | [Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/normal.tgz) | 0.3 | [Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/normal.zip) | 0.3 |
| **Horizontal Misalignment** | [Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/horizontal-misalignment.tgz) | 1.4 | [Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/horizontal-misalignment.zip) | 1.4 |
| **Vertical Misalignment** | [Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/vertical-misalignment.tgz) | 2.1 | [Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/vertical-misalignment.zip) | 2.1 |
| **Imbalance** | [Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/imbalance.tgz) | 2.3 |[Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/imbalance.zip) | 2.3 |
| **Underhang Bearing** | [Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/underhang.tgz) | 3.7 | [Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/underhang.zip) | 3.7 |
| **Overhang Bearing** | [Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/overhang.tgz) | 3.4 | [Download](http://www02.smt.ufrj.br/~offshore/mfs/database/mafaulda/overhang.zip) | 3.4 |

---

[_MAFAULDA_](http://www02.smt.ufrj.br/~offshore/mfs/index.html#TOC1)
