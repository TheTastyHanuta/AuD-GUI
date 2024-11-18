# AuD-GUI

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Structure](#structure)
4. [Run](#run)
5. [Settings](#settings)
6. [Functionalities](#functionalities)
7. [Acknowledgments](#acknowledgments)

## Prerequisites
1. Download and install [Git](https://git-scm.com/downloads/).
2. Download and install [Python](https://www.python.org/downloads/) and add it to PATH (=> restart your device).

## Setup
1. Open the terminal on your computer and navigate to a folder of your choice where the GUI and its data should be stored (Use the `cd` command to change the directory).
2. Clone the current repository state by executing the following command in the terminal:
   ```bash
   git clone https://github.com/sikr02/AuD-GUI.git
   ```
   If that command ran sccessfully, then the source code and all data should have been copied to the local folder.
   
   The structure should look as follows:
   ```
   ./AuD-GUI
     ├── .tmp
     │    └── .gitkeep
     ├── data
     │    └── .gitkeep
     ├── logs
     │    └── .gitkeep
     ├── out
     │    └── .gitkeep
     ├── settings
     │    └── .gitkeep
     │
     ├── src
     │    ├── comment_utils.py
     │    ├── convert_txt_to_json.py
     │    ├── dialogs.py
     │    ├── gui_utils.py
     │    ├── io_utils.py
     │    └── manager.py
     │
     ├── templates
     │    ├── 01_helloworld_circuit.json
     │    ├── ...
     │    └── 09_binarysearchtree.json
     │
     ├── txt_templates
     │    ├── 01_helloworld_circuit.txt
     │    ├── ...
     │    └── 09_binarysearchtree.txt
     │
     ├── .gitignore
     ├── LICENSE
     ├── README.md
     ├── gui.py
     └── requirements.txt
   ```
   
## Structure
A short description of the folders and files:
- `data`: In this folder, all correction data is stored. These are the files that change, if you add or remove points. Also these files are used for the export.
- `logs`: The GUI logs pretty much during activity, so if you encounter an error, have a look inside the latest log.
- `out`: The export structure and the zipped export files are put into this folder. These zip files have to be uploaded on StudOn.
- `settings`: After starting the GUI for the first time, you will find a `settings.json` file in there, where the personal annotation is stored. Further settings content may follow.
- `src`: Here you find all source files. ***Stay away from the source code unless you know what you're doing!***
- `templates`: In here, there are all the comment templates in a structured JSON form.
- `txt_templates`: The templates in text form for better readability. *Change the templates yourself:* If you want to do so, use `convert_txt_to_json.py` to make changes to the templates. Write in the text templates, execute the file and the use the updated JSON template (The templates follow a specific structure, so there is no guarantee for your adaptions to work !).

## Run
To run the GUI, execute `gui.py` by writing the following command into the terminal:
```bash
python <path_to_gui>/AuD-GUI/gui.py
```
If you have no python IDE installed, then double clicking on the file may also work.

## Settings
If you start the GUI for the first time, go to the `Datei > Einstellungen` menu and set the personal annotation. 
This annotation is added to every text feedback as a kind of "signature". Enter your personal information and save it.

## Functionalities
A quick overview on the current functionalities:
- **Import**: Import the students' submissions as folder (`Datei > Abgaben importieren > Ordner`) or zip archive (`Datei > Abgaben importieren > Zip-Datei`).
  - Choose a comment template
  - Enter the team IDs that were assigned to you
- **Open**: Open previously imported submissions via `Datei > Korrektur öffnen`.
- **Navigation menu**:
  - `Navigation > Nächstes Team`: Jumps to the next team
  - `Navigation > Vorheriges Team`: Jumps to the previous team
  - `Navigation > Suche Team`: Searches for a user defined ID in the list of all IDs
  - `Navigation > PDF öffnen`: One of the most important options. It opens the `Korrektur.pdf`-File for the current team. Write your comments in there and ***save it in the same location where it was before (!)***. Otherwise, the GUI will not find the file anymore.
- **Export**: After finishing the correction, export the results via (`Datei > Korrekturen exportieren`).
  - Define the name of the export folder (StudOn only accepts a specified filename)
  - Let the GUI open the location where the output is stored and copy the location of the zip file
  - Upload the zip file on StudOn. You will get a quick overview on what you are uploading. Double check, if all Teams and PDFs are included
  - Upload => Finished :D

## Acknowledgments
- This project is quite experimental, so you may encounter some bugs. ¯\\\_(ツ)_/¯
- If you encounter such a bug, please start a GitHub issue and report the bug.
- To update your GUI to the latest version, navigate to the local `AuD-GUI` folder and execute:
   ```bash
   git pull
   ```
- A detailed description of the procedures with pictures may follow in the future ... :D

State: 24-11-18, Author: Simon Kramer