# ard-transformer
Transforming data generated from CA ARD to ALM Octane

## Purpose
This custom solution bridges the gap between two widely known tools in the market, namely CA Agile Requirements Designer [ARD] and MicroFocus ALM Octane.

Currently, CA ARD provides an integration capability with HP QC/ALM and automatically uploads the test cases generated from ARD to QC/ALM. However, this is a limitation in CA ARD and does not integrate with the advanced version of QC/ALM, which is MicroFocus ALM Octane. 

The custom solution written in Python will read the data generated from CA ARD [.xlsx], transform and write the data [.xlsx] to Octane undestandable format. The transformed data in [.xlsx] is further used for import into ALM Octane. 

![Transformer](https://upload.wikimedia.org/wikipedia/commons/6/60/ARD-Octane.jpg)


## Usage

#### Prerequisites
1. Python Intepreter to be installed on the machine where this utility is planned to be run. Python can be downloaded from https://www.python.org/downloads/
2. Download the utility program [transform.py] 
3. Availability of input data [alm.xlsx] in the same location where the utility program is made available.

#### Execution
1. Run the utility program in the following way 

       python transform.py

2. Below are logs generated

       Transformation started...please wait
       Transformation Completed
       
3. A new file [octane.xlsx] is generated in the same location of utility program after the transformation is complete. 
