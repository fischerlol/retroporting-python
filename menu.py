import shutil
import sys
import keyboard
import config
import os
import os.path
import glob
import subprocess
from rich import print as printc
from rich.console import Console
from utils.functions import print_addition, print_deletion, delete_files, check_empty_path, \
    copy_files, run_script, git_clone, unzip

console = Console()


def menu():
    print('-' * 30)
    print(('-' * 13) + 'Menu' + ('-' * 13))
    print('I. Initial setup')
    print('W. Launch WoW.Export')
    print('1. Run MultiConverter')
    print('2. Run Helmet Fix')
    print('3. Run SQL queries and Headless Exporter')
    print('4. Move converted files to MPQ patch')
    print('5. Clear working directories')
    print('6. Clear cache and launch wow')
    print('7. Clear cache')
    print('Q. Exit')
    return input(': ')


def one():
    # create directory if it doesn't exist
    if not os.path.exists(config.multi_converter_path_2):
        os.mkdir(config.multi_converter_path_2)

    # check if path is the right size for deletion
    check_empty_path(config.multi_converter_path_2, 'one_delete')

    # print deletions
    print_deletion(config.multi_converter_path_2, '')

    # delete old files
    delete_files(config.multi_converter_path_2)

    # check if path is the right size for addition
    check_empty_path(config.wow_export_path, 'one_add')

    # print additions
    print_addition(config.wow_export_path)

    # copy files from wow.export to multiconverter
    copy_files(config.wow_export_path, config.multi_converter_path_2)

    # run multiconverter
    os.chdir(config.multi_converter_path_1)
    for files in glob.glob(config.multi_converter_path_1 + '/**/*.m2', recursive=True):
        args = [config.multi_converter_path_1 + '/MultiConverter_Console.exe', '-fixhelm', files]
        multi_convert = subprocess.Popen(args)
        multi_convert.wait(keyboard.press_and_release('enter'))


def two():
    # create directory if it doesn't exist
    if not os.path.exists(config.multi_converter_path_2):
        os.mkdir(config.multi_converter_path_2)

    # check if path is the right size for deletion
    check_empty_path(config.multi_converter_path_2, 'two_delete')

    # print deletions
    print_deletion(config.multi_converter_path_2, '')

    # delete old files
    delete_files(config.multi_converter_path_2)

    # check if path is the right size for addition
    check_empty_path(config.wow_export_helmet_path, 'two_add')

    # print additions
    print_addition(config.wow_export_helmet_path)

    # copy files from wow.export to multiconverter
    copy_files(config.wow_export_helmet_path, config.multi_converter_path_2)

    # run multiconverter
    os.chdir(config.multi_converter_path_1)
    for files in glob.glob(config.multi_converter_path_1 + '/**/*.m2', recursive=True):
        args = [config.multi_converter_path_1 + '/MultiConverter_Console.exe', '-fixhelm', files]
        multi_convert = subprocess.Popen(args)
        multi_convert.wait(keyboard.press('enter'))


def three():
    # blank line
    print('')

    # run items.sql script
    run_script('items.sql', config.sql_path_items, config.world_database)

    # run item-dbc.sql script
    run_script('item-dbc.sql', config.sql_path_item_dbc, config.dbc_database)

    # run itemdisplayinfo-dbc.sql script
    run_script('itemdisplayinfo-dbc.sql', config.sql_path_item_display_info_dbc, config.dbc_database)

    # print program running
    printc('\n[yellow]Running Headless Exporter:\n[/yellow]')

    # run headless exporter
    os.chdir(config.headless_export_path)
    args = [config.headless_export_path + '/HeadlessExport.exe']
    headless_export = subprocess.Popen(args)
    headless_export.wait(keyboard.press('enter'))


def four():
    # check if patch exists
    # check_empty_patch(config.data_path)

    # check if path is the right size for addition
    check_empty_path(config.wow_export_path, 'four_add')

    # check if path is the right size for addition
    check_empty_path(config.wow_export_helmet_path, '')

    # print additions
    print_addition(config.wow_export_path)

    # print additions
    print_addition(config.wow_export_helmet_path)

    # copy files from wow.export to patch folder
    copy_files(config.wow_export_path, config.patch_path)

    # copy files from wow.export.helmet to patch folder
    copy_files(config.wow_export_helmet_path, config.patch_path)


def five():
    # check if path is the right size for deletion
    check_empty_path(config.wow_export_path, 'five_delete')
    check_empty_path(config.wow_export_helmet_path, 'five_delete_1')
    check_empty_path(config.multi_converter_path_2, 'five_delete_2')

    # print deletions
    print_deletion(config.wow_export_path, 'five_delete_3')
    print_deletion(config.wow_export_helmet_path, '')
    print_deletion(config.multi_converter_path_2, '')

    # delete files in current working directory
    delete_files(config.wow_export_path)
    delete_files(config.wow_export_helmet_path)
    delete_files(config.multi_converter_path_2)


def six():
    # change directory
    os.chdir(config.wow_path)

    # check if cache exists
    if os.path.exists(config.cache_path):
        shutil.rmtree('Cache')
        printc('\n[red][-][/red] Cache deleted')
    else:
        printc('\n[yellow][!][/yellow] Cache does not exist\n')

    # open wow
    printc('[green][+][/green] Launching WoW\n')
    subprocess.Popen(config.wow_exe_path)


def seven():
    # change directory
    os.chdir(config.wow_path)

    # check if cache exists
    if os.path.exists(config.cache_path):
        # delete cache
        shutil.rmtree('Cache')
        printc('\n[red][-][/red] Cache deleted\n')
    else:
        printc('\n[yellow][!][/yellow] Cache does not exist\n')


def initial_setup():
    # clone/update repo
    git_clone(config.patch_repo_1, config.patch_repo_2)

    # copy files from patch repo to patch directory
    copy_files(config.patch_repo_1 + '/patch', config.default_path + '/patch')

    # run makefile
    os.chdir(config.patch_repo_3)
    make_process1 = subprocess.Popen('make all', shell=True, stdout=subprocess.PIPE,
                                     stderr=sys.stdout.fileno())
    printc('[green][+][/green] Running makefile:')
    while True:
        line = make_process1.stdout.readline()
        if not line:
            break
        sys.stdout.flush()
    print()

    # unzip .7z archives
    unzip(config.converting_tools, 'BLP Converter.7z')
    unzip(config.converting_tools, 'MultiConverter.7z')
    unzip(config.converting_tools, 'Spell Editor.7z')
    unzip(config.converting_tools, 'WoW.Export.7z')
    print()


def wow_export():
    # launch wow.export
    subprocess.Popen(config.wow_export_exe_path)
