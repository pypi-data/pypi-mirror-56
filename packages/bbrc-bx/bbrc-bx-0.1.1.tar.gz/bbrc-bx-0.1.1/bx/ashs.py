from datetime import datetime
import os.path as op
import logging as log
from bx.parse import Command
from bx import parse


class ASHSCommand(Command):
    nargs = 2
    resource_name = 'ASHS'

    def __init__(self, *args, **kwargs):
        super(ASHSCommand, self).__init__(*args, **kwargs)

    def parse(self, test=False):
        subcommand = self.args[0]
        id = self.args[1] #should be a project or an experiment_id
        print(id)
        if subcommand in ['volumes']:
            self.subcommand_aparc(test)

        elif subcommand in ['files', 'report', 'snapshot']:
            self.subcommand_download(test)

        elif subcommand == 'tests':
            from bx.validation import subcommand_tests
            subcommand_tests(parser=self, test=test, validator='ASHSValidator',
                version=['##0390c55f', '4e37c9d0'])

    def subcommand_aparc(self, test=False):
        subcommand = self.args[0]
        id = self.args[1]

        if subcommand == 'volumes':
            df = parse.download_measurements(self.xnat, ashs_measurements,
                id, test, resource_name=self.resource_name)

        dt = datetime.today().strftime('%Y%m%d_%H%M%S')
        fn = 'bx_%s_%s_%s_%s.xlsx'%(self.command, subcommand, id, dt)
        fp = op.join(self.destdir, fn)
        log.info('Saving it in %s'%fp)
        df.to_excel(fp)


    def subcommand_download(self, test=False):
        ''' following subcommands: files, report and snapshot '''

        subcommand = self.args[0]
        id = self.args[1]

        validation_report = 'ASHSValidator'

        resource_name = self.resource_name if  subcommand != 'report' else None

        if subcommand in ['files', 'report']:
            parse.download_experiments(self.xnat, id, resource_name,
                validation_report, self.destdir, self.overwrite,
                test=test)

        elif subcommand in ['snapshot']:
            parse.download_snapshots(self.xnat, id, validation_report,
                self.destdir, self.overwrite, test=test)


def ashs_measurements(x, experiments, resource_name='ASHS'):
    from tqdm import tqdm
    import pandas as pd

    table = []
    for e in tqdm(experiments):
        log.debug(e)
        try:
            s = e['subject_label']
            r = x.select.experiment(e['ID']).resource(resource_name)
            if not r.exists():
                log.error('%s has no %s resource'%(e, resource_name))
                continue
            volumes = r.volumes()
            volumes['subject'] = s
            volumes['ID'] = e['ID']
            table.append(volumes)
        except KeyboardInterrupt:
            return pd.concat(table).set_index('ID').sort_index()
        except Exception as exc:
            log.error('Failed for %s. Skipping it.'%e)
            log.error(exc)
            continue
    hippoSfVolumes = pd.concat(table).set_index('ID').sort_index()
    return hippoSfVolumes
