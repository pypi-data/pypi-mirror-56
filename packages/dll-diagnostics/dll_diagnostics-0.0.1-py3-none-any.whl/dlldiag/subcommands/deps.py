from ..common import ModuleHeader, OutputFormatting, WindowsApi
from termcolor import colored
import argparse, os, sys

def deps():
	
	# Our supported command-line arguments
	parser = argparse.ArgumentParser(prog='{} deps'.format(sys.argv[0]))
	parser.add_argument('module', help='DLL or EXE file for which direct dependencies will be loaded')
	
	# If no command-line arguments were supplied, display the help message and exit
	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit(0)
	
	# Parse the supplied command-line arguments
	args = parser.parse_args()
	
	try:
		
		# Parse the PE header for the module
		print('Parsing module header and identifying direct dependencies... ', end='')
		header = ModuleHeader(args.module)
		architecture = header.getArchitecture()
		dependencies = header.listDependencies()
		print('done.\n')
		
		# Display the module details
		print('Parsed module details:')
		OutputFormatting.printModuleDetails(header)
		print()
		
		# Iterate over each of the module's dependencies and attempt to load them
		cwd = os.path.dirname(args.module)
		columnWidth = max([len(dll) for dll in dependencies]) + 4
		print('Attempting to load the module\'s direct dependencies:\n', flush=True)
		for dll in dependencies:
			result = WindowsApi.loadModule(dll, cwd, architecture)
			OutputFormatting.printRow(dll, OutputFormatting.formatColouredResult(result, [dll], 'Loaded successfully'), width=columnWidth)
			sys.stdout.flush()
		
		# Display the error propagation notice
		print(colored('\n\nImportant note regarding errors:\n', color='yellow'))
		print('Errors loading indirect dependencies are propagated by LoadLibrary(), which')
		print('means any errors displayed above that indicate missing or corrupt modules may')
		print('in fact be referring to a child dependency of a direct dependency, rather than')
		print('the direct dependency itself.\n')
		print('Use the `{} trace` command to inspect loading errors for a module in detail.'.format(sys.argv[0]))
		sys.stdout.flush()
		
	except RuntimeError as e:
		print('Error: {}'.format(e))
		sys.exit(1)


DESCRIPTOR = {
	'function': deps,
	'description': 'Lists the direct dependencies for a module and checks if they can be loaded'
}
