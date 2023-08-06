import logging as log
from datetime import datetime
import os.path as op
from bx.parse import Command


class CAT12Command(Command):
    nargs = 2
    resource_name = 'CAT12_SEGMENT'


    def __init__(self, *args, **kwargs):
        super(CAT12Command, self).__init__(*args, **kwargs)

    def parse(self, test=False):
        subcommand = self.args[0]
        id = self.args[1]

        if subcommand in ['files', 'report', 'snapshot']:
            self.subcommand_download(test)

        elif subcommand == 'volumes':
            self.subcommand_volumes(test)

        elif subcommand == 'tests':
            from bx.validation import subcommand_tests
            subcommand_tests(parser=self, test=test, validator='CAT12SegmentValidator',
                version=['##0390c55f', '2bc4d861'])



    def subcommand_download(self, test=False):
        subcommand = self.args[0]
        id = self.args[1]

        validation_report = 'CAT12SegmentValidator'
        resource_name = self.resource_name if  subcommand != 'report' else None

        from bx import parse
        if subcommand in ['files', 'report']:
            parse.download_experiments(self.xnat, id, resource_name,
                validation_report, self.destdir, self.overwrite, test=test)
        elif subcommand in ['snapshot']:
            parse.download_snapshots(self.xnat, id, validation_report,
                self.destdir, self.overwrite, test=test)


    def subcommand_volumes(self, test=False):

        subcommand = self.args[0]
        id = self.args[1]

        from bx import parse
        df = parse.download_measurements(self.xnat, cat12_volumes, id, test,
            resource_name='CAT12_SEGMENT')

        dt = datetime.today().strftime('%Y%m%d_%H%M%S')
        fn = 'bx_%s_%s_%s_%s.xlsx'%(self.command, subcommand, id, dt)
        fp = op.join(self.destdir, fn)
        log.info('Saving it in %s'%fp)
        df.to_excel(fp)


def cat12_volumes(x, experiments, resource_name):
    from tqdm import tqdm
    import pandas as pd
    import tempfile
    import nibabel as nib
    import numpy as np
    import os

    table = []

    for e in tqdm(experiments):
        log.debug(e)
        try:
            r = x.select.experiment(e['ID']).resource(resource_name)
            if not r.exists():
                log.error('%s has no %s resource'%(e['ID'], resource_name))
                continue
            vols = [e['ID']]
            for kls in ['p1', 'p2', 'p3']:

                f = [each for each in r.files('mri/%s*'%kls)][0]
                fp = tempfile.mkstemp('.nii.gz')[1]
                f.get(fp)
                d = nib.load(fp)
                size = np.prod(d.header['pixdim'].tolist()[:4])
                v = np.sum(d.dataobj) * size
                os.remove(fp)
                vols.append(v)
            table.append(vols)

        except KeyboardInterrupt:
            return pd.DataFrame(table, columns=['ID', 'c1', 'c2', 'c3']).set_index('ID').sort_index()
        except Exception as exc:
            log.error('Failed for %s. Skipping it.'%e)
            log.error(exc)
            continue

    df = pd.DataFrame(table, columns=['ID', 'c1', 'c2', 'c3']).set_index('ID').sort_index()
    return df
