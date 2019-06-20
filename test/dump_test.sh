# Dump the contents of the factory, Synthmania and hAQ_aTTAQ packs...

find 'Factory 21-100'/ -name '*.unosyp' -exec bash -c "echo '{}';python ../uno_synth.py -d '{}'" \; >> factory_dump.txt
find Synthmania/ -name '*.unosyp' -exec bash -c "echo '{}';python ../uno_synth.py -d '{}'" \; >> synthmania_dump.txt
find '80_UNO_Synth_ presets_by_haQ_attaQ'/ -name '*.unosyp' -exec bash -c "echo '{}';python ../uno_synth.py -d '{}'" \; >> haq_attaq_dump.txt
