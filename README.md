# 🏃 Runcorder - Running Training Management System
A program used to record daily running records for runners, marathon enthusiasts and college sports enthusiasts.

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

> A localized running training management system based on Tkinter, supporting user management, training logging, data analysis and visualization.

## 🌟 Core Features

### 👥 User Management
- **Multi-user System**: Create/load/delete user profiles
- **Independent Data Storage**: Each user's data stored in separate JSON files
- **Input Validation**: Ensures data integrity through format verification

### 📝 Training Logging
- **Comprehensive Records**: Track date, distance, pace, self-assessment, and morning run markers
- **Smart Input Handling**:
  - Supports `5/30` or `5` pace formats
  - Automatic date validation (YYYY-MM-DD)
  - Distance range checking

### 📊 Data Analysis
- **Interactive Charts**:
  - Running distance trend line
  - Average pace curve
  - Custom Y-axis range adjustment
- **Multi-dimensional Table**:
  - Date-sorted training records
  - Training mode annotations
  - Morning/Non-morning run statistics

### 🛠️ Advanced Features
- **Record Management**: Modify/delete historical entries
- **Training Modes**: 4 preset modes (Aerobic/Anaerobic/Mixed)
- **Data Persistence**: JSON storage with cross-platform compatibility

---

## 🛠️ Technology Stack

- **Core Framework**: Tkinter GUI
- **Data Processing**: Pandas/Numpy
- **Visualization**: Matplotlib
- **Table Generation**: Tabulate
- **Architecture**: MVC Layered Design
