import logging

from composer.efile.update import UpdateEfileState

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

update: UpdateEfileState = UpdateEfileState.build("/Volumes/bulk/efile")
update()
