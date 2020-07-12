import argparse
import glob
import re
import os


parser = argparse.ArgumentParser(description='Convert chat files to txt')
parser.add_argument('--chatdir', metavar='DIR',
                    help='path to dir with chat files', default='./')
parser.add_argument('--output', metavar='DIR',
                    help='path to outpt', default='./')


if __name__ == '__main__':
    args = parser.parse_args()
    
    chatfiles = glob.glob(args.chatdir)
    for f in chatfiles:
    	filename_w_ext = os.path.basename(f)
    	filename, file_extension = os.path.splitext(filename_w_ext)
    	of = open(args.output+"/"+filename+".txt","w")
    	
    	with open(f) as fp:  
    		line = fp.readline()
    		while line:
    			if re.match(r'\*PAR\:', line):
    				# throat clears
    				line = re.sub(r'\&\=clears\s+throat',r' ',line) # throat clears
    				line = re.sub(r'(\w+)\((\w+)\)',r'\1\2',line) # open parentheses e.g, comin(g)
    				line = re.sub(r'\((\w+)\)(\w+)',r'\1\2',line) # open parentheses e.g, (be)coming
    				line = re.sub(r'\s+\w+\s+\[\:\s+([^\]]+)\]',r' \1 ', line) # open square brackets eg. [: overflowing] - error replacements
    				line = re.sub(r'\&\w+\s+',r' ', line) # remove disfluencies prefixed with "&"
    				line = re.sub(r'xxx',r' ', line) # remove unitelligible words
    				line = re.sub(r'\(\.+\)',r' ', line) # remove pauses eg. (.) or (..)
    				line = re.sub(r'\[\/+\]',r' ', line) # remove forward slashes in square brackets
    				line = re.sub(r'\&\=\S+\s+',r' ', line) # remove noise indicators eg. &=breath
    				
    				line = re.sub(r'\*PAR\:',r' ', line) # remove turn identifiers
    				line = re.sub(r'\[(\*|\+|\%)[^\]]+\]',r' ', line) # remove star or plus and material inside square brackets indicating an error code
    				line = re.sub(r'\[(\=\?)[^\]]+\]',r' ', line)
    				
    				line = re.sub(r'[^A-Za-z\n \']','',line) # finally remove all non alpha characters
    				
    				#line = "<s> "+ line + "</s>" # format with utterance start and end symbols
    				line = re.sub(r'\s+',' ',line) # replace multiple spaces with a single space
    				line = line.lower() # lowercase
    				
    				# write it out
    				if line != '<s> </s>' and line != '<s></s>' :				
	    				of.write(line+"\n")
    				
    			line = fp.readline()
    	
    	of.close()
    	
    
    
