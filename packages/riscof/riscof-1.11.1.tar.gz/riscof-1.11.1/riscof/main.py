import logging
import importlib
from datetime import datetime
import os
import pytz
import shutil
import configparser

from jinja2 import Template

import riscof
import riscv_config.checker as riscv_config
import riscof.framework.main as framework
import riscof.framework.test as test_routines
import riscof.utils as utils
import riscof.constants as constants
from riscv_config.errors import ValidationError


def execute():
    '''
        Entry point for riscof. This function sets up the models and 
        calls the :py:mod:`riscv_config` and :py:mod:`framework` modules with 
        appropriate arguments.
    '''
    # Set up the parser
    parser = utils.riscof_cmdline_args()
    args = parser.parse_args()

    # Set up the logger
    utils.setup_logging(args.verbose)
    logger = logging.getLogger()
    logger.handlers = []
    ch = logging.StreamHandler()
    ch.setFormatter(utils.ColoredFormatter())
    logger.addHandler(ch)
    fh = logging.FileHandler('run.log', 'w')
    logger.addHandler(fh)


    if (args.run or args.testlist or args.validateyaml):
        config = configparser.ConfigParser()
        logger.info("Reading configuration.")
        try:
            config.read('config.ini')
        except FileNotFoundError as err:
            logger.error(err)
            return 1

        riscof_config = config['RISCOF']
        logger.info("Preparing Models")
        # Gathering Models
        dut_model = riscof_config['DUTPlugin']
        base_model = riscof_config['ReferencePlugin']
        logger.debug("Importing " + dut_model + " plugin")
        dut_plugin = importlib.import_module("riscof_" + dut_model)
        dut_class = getattr(dut_plugin, dut_model)
        if dut_model in config:
            dut = dut_class(name="DUT", config=config[dut_model])
        else:
            dut = dut_class(name="DUT")
        logger.debug("Importing " + base_model + " plugin")
        base_plugin = importlib.import_module("riscof_" + base_model)
        base_class = getattr(base_plugin, base_model)
        if base_model in config:
            base = base_class(name="Reference", config=config[base_model])
        else:
            base = base_class(name="Reference")

        #Run riscv_config on inputs
        isa_file = dut.isa_spec
        platform_file = dut.platform_spec

        work_dir = constants.work_dir
        #Creating work directory
        if not os.path.exists(work_dir):
            logger.debug('Creating new work directory: ' + work_dir)
            os.mkdir(work_dir)
        else:
            logger.debug('Removing old work directory: ' + work_dir)
            shutil.rmtree(work_dir)
            logger.debug('Creating new work directory: ' + work_dir)
            os.mkdir(work_dir)

        try:
            isa_file, platform_file = riscv_config.check_specs(
                isa_file, platform_file, work_dir, True)
        except ValidationError as msg:
            logger.error(msg)
            return 1

        if(args.validateyaml):
          exit(0)
        
        report_objects = {}
        report_objects['date'] = (datetime.now(
            pytz.timezone('GMT'))).strftime("%Y-%m-%d %H:%M GMT")
        report_objects['version'] = riscof.__version__
        report_objects['dut'] = (dut.__model__).replace("_", " ")
        report_objects['reference'] = (base.__model__).replace("_", " ")

        isa_specs = utils.load_yaml(isa_file)
        platform_specs = utils.load_yaml(platform_file)

        if(args.testlist):
            test_routines.generate_test_pool(isa_specs, platform_specs)
            return 0

        with open(isa_file, "r") as isafile:
            ispecs = isafile.read()

        with open(platform_file, "r") as platfile:
            pspecs = platfile.read()

        report_objects['isa'] = isa_specs['ISA']
        report_objects['usv'] = isa_specs['User_Spec_Version']
        report_objects['psv'] = isa_specs['Privilege_Spec_Version']
        report_objects['isa_yaml'] = isa_file
        report_objects['platform_yaml'] = platform_file
        report_objects['isa_specs'] = ispecs
        report_objects['platform_specs'] = pspecs

        report_objects['results'] = framework.run(dut, base, isa_file,
                                                  platform_file)

        report_objects['num_passed'] = 0
        report_objects['num_failed'] = 0

        for entry in report_objects['results']:
            if entry['res'] == "Passed":
                report_objects['num_passed'] += 1
            else:
                report_objects['num_failed'] += 1

        with open(constants.html_template, "r") as report_template:
            template = Template(report_template.read())

        output = template.render(report_objects)

        reportfile = os.path.join(constants.work_dir, "report.html")
        with open(reportfile, "w") as report:
            report.write(output)

        shutil.copyfile(constants.css,
                        os.path.join(constants.work_dir, "style.css"))

        try:
            import webbrowser
            webbrowser.open(reportfile)
        except:
            return 0
    elif (args.setup):
        logger.info("Setting up environment files.")
        try:
            logger.debug(
                "Copying sample directory containing environment files.")
            cwd = os.getcwd()
            src = os.path.join(constants.root, "Templates/setup/env/")
            dest = os.path.join(cwd, "env/")
            shutil.copytree(src, dest)
            logger.debug("Copying sample config file.")
            src = os.path.join(constants.root, "Templates/setup/config.ini")
            shutil.copy(src, cwd)
            return 0
        except FileExistsError as err:
            logger.error(err)
            return 1


if __name__ == "__main__":
    exit(execute())
