from os.path import  basename, isfile, join
import os
import sys
import glob
import argparse		
import shaonutil

def get_members(module):
	return [member for member in dir(module) if callable(getattr(module, member))]

def get_file_description_file(module):
	member_doc_dic = {}
	for member in get_members(module):
		if getattr(module, member).__doc__ != None:
			member_doc_dic[member] = getattr(module, member).__doc__
	return member_doc_dic

def createNewReadme():
	name = input("Project Name:")
	tag = input("Project Tag:")
	author = input("Project Author:")
	contact = input("Project Contact:")
	installation = input("Installation Link/String:")
	
	final_string_to_save = f"""## {name} - {tag}
Author: {author} - {contact}
## Utilities

## Installation
{installation}
## Function Usages

Function Usages End"""
	return final_string_to_save

def generateFunctionUsagesString(realcurrentpath):
	#list all py modules in current directory
	all_py_files = glob.glob(join(realcurrentpath, "*.py"))
	allmodules = [basename(c)[:-3] for c in all_py_files if isfile(c) and not c.endswith('__init__.py')]

	#get function usages lines
	func_usages_string = ''
	for m in allmodules:
		module_heading = '### '+m+'\n\n'
		module = __import__(m)
		member_doc_dic = get_file_description_file(module)
		func_lines = ''
		for member in member_doc_dic:
			func_lines += member + ' - ' + member_doc_dic[member] + '\n\n'
		func_usages_string += module_heading + func_lines

	return func_usages_string

def init(args):
	printline=False

	realcurrentpath = os.path.realpath('')
	sys.path.append(realcurrentpath)

	if args.output:
		outputfile = args.output
	else:
		outputfile = 'docu.md'

	outputfile = os.path.join(realcurrentpath, outputfile)

	if args.readme == 'bare':
		alllines = createNewReadme()
	else:
		readmefilename = args.readme
		filerealpath = os.path.join(realcurrentpath, readmefilename)

		func_usages_string = generateFunctionUsagesString(realcurrentpath)

		start = '## Function Usages'
		end = 'Function Usages End'
		# read the contents of your README file
		with open(filerealpath, encoding='utf-8') as file:
		    lines = file.readlines()
		#getting the existing func usages lines in readme file
		count = 0
		startc = 0
		endc = 0
		for c in lines:
			if start in c:
				startc = count
			if end in c:
				endc = count
				break
			count+=1
		deductlines = ''.join( lines[startc+1:endc] )

		#replacing existing lines with prepared lines
		alllines = ''.join(lines)

	final_string_to_save = alllines.replace(deductlines,func_usages_string)


	if(printline):print(final_string_to_save)
	shaonutil.file.write_file(outputfile, final_string_to_save,mode="w")

def main():
	parser = argparse.ArgumentParser(description="Automatic Documentation Generator")
	parser.add_argument("--readme", help="input the sample readme file",type=str,required=True)
	parser.add_argument("--output", help="input the outputfile file",type=str)
	args = parser.parse_args()
		
	try:
		init(args)
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	main()
