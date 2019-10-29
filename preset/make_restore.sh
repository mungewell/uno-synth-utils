mkdir Factory\ 21-100/restore
mkdir 80_UNO_Synth_\ presets_by_haQ_attaQ/restore
mkdir ADSR\ Urban/restore
mkdir KC\ Gilmore/restore
mkdir Synthmania/restore
mkdir UNO_Synth_Presets_By_Blandy/restore

python3 process.py -i Factory\ 21-100/ > Factory\ 21-100/restore/restore.sh
python3 process.py 80_UNO_Synth_\ presets_by_haQ_attaQ/ > 80_UNO_Synth_\ presets_by_haQ_attaQ/restore/restore.sh
python3 process.py ADSR\ Urban/ > ADSR\ Urban/restore/restore.sh
python3 process.py KC\ Gilmore/ > KC\ Gilmore/restore/restore.sh
python3 process.py Synthmania/ > Synthmania/restore/restore.sh
python3 process.py UNO_Synth_Presets_By_Blandy/ > UNO_Synth_Presets_By_Blandy/restore/restore.sh
