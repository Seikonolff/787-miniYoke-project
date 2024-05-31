# 787 miniYoke Project

## Description

Simple yoke's avionic simulation project made out of 4 python scripts :
- Flight management system (FMS)
- Automatic pilot in longitudinal axis
- Automatic pilot in lateral axis
- Yoke simulation <-- This repo

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

make sure to install the following dependencies : 
- pip install ivy - python
- pip install enum34
- pip install pygame

## Usage

The module is set to work along the 3 others to complete a flight in a simulated environnement hosted on a web-page.

On MacOs/linux (not suported atm) :
- open terminal :
    - chmod +x aircraft-sim
    - ./aircraft-sim --bus "bus's IP adress" (prod : "224.255.255.255:2010" test : "127.0.0.1:8000")
    - allow application in system settings if required
    - python3 main.py

On Windows :
- in local host :
    - launch the .exe file
- in a specific adress : 
    - aircraft-sim.exe --bus "adress"
- open terminal :
    - python3 main.py

## Contributing

Only Enac students are able to contribute to this project

## License

This project is not licensed and is provided as-is without any warranty.