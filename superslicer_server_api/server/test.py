import os
from os.path import join, dirname, abspath

ROOT_FOLDER = dirname(dirname(abspath(__file__)))
FILES_FOLDER = join(ROOT_FOLDER, "files")
STL_FOLDER = join(FILES_FOLDER, "stls")
GCODE_FOLDER = join(FILES_FOLDER, "gcodes")

# if os.path.isdir(gcodes_path):
#    print(gcodes_path)
# if os.path.isdir(stls_path):
#    print(stls_path)
cmd_list = ['superslicer', '-g']
print("ROOT-----------------------------")
print(ROOT_FOLDER)
print("\nFILES----------------------------")
print(FILES_FOLDER)
print("\nSTL------------------------------")
print(STL_FOLDER)
print("\nGCODE----------------------------")
print(GCODE_FOLDER + "\n")

stl_files = os.scandir(STL_FOLDER)

existed = False
filename = 'filerequest.py'
with stl_files:
    for entry in stl_files:
        existed = entry.name == filename and entry.is_file()
        if existed:
            os.remove(join(STL_FOLDER, filename))
            break

if existed:
    print({'message': f'File {filename} deleted successfully'})
else:
    print({'message': 'The file specified does not exist'})
