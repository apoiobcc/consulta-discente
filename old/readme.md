# CDE results extractor

- The results of the CDE must be in the file `results.csv`
- Run `python3 generate_plots.py` to generate one folder for each discipline
    - Each folder will have the comments of remote classes and general classes opinions in `.txt` files
    - Will also contain a `name.txt` file with the fill description of the discipline
    - Finally it contains `.png` images for each graph generated
- In the root directory there are two files `ensino_geral.md` and `ensino_remoto.md`. Those files are templates for the final reports
- Run `bash generate_pdf.sh` to generate final `.pdf` files that contains the results. All the final pdfs will be in the `reports/` folder
- If any censorship is necessary in the comments made by students, it is necessary to update the `.txt` files in the discipline folder and rerun the bash script 