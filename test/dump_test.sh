# Dump the contents of the factory, Synthmania and hAQ_aTTAQ packs...

find 'Factory 21-100'/ -name '*.unosyp' -exec bash -c "echo '{}';python ../uno_synth.py -d '{}'" \; >> factory_dump.txt
find Synthmania/ -name '*.unosyp' -exec bash -c "echo '{}';python ../uno_synth.py -d '{}'" \; >> synthmania_dump.txt
find '80_UNO_Synth_ presets_by_haQ_attaQ'/ -name '*.unosyp' -exec bash -c "echo '{}';python ../uno_synth.py -d '{}'" \; >> haq_attaq_dump.txt
find 'UNO_Synth_Presets_By_Blandy'/ -name '*.unosyp' -exec bash -c "echo '{}';python ../uno_synth.py -d '{}'" \; >> blandy_dump.txt
find 'ADSR Urban'/ -name '*.unosyp' -exec bash -c "echo '{}';python ../uno_synth.py -d '{}'" \; >> adsr_urban.txt
