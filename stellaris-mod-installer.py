import zipfile
import shutil
import glob
import os

PATH = os.path.split(__file__)[0]
max_count = len(glob.glob("*.zip"))
count = 1
for file_name in glob.glob("*.zip"):
    name = file_name.split("_")
    name[-1] = name[-1].replace(".zip", "")
    id_number = name[0]
    name = " ".join(name[1:]).capitalize()
    
    print(f"Installing {file_name} | {count}/{max_count}")
    print(f" > Started the reading of file {file_name}")
    try:
        with zipfile.ZipFile(file_name) as z:
            print(f" > Unzipping {name} with id {id_number}")
            z.extractall(path=id_number)
            print(f" > Succesful extraction")
    except:
        print(f" ! Unsuccesful extraction of file {file_name}".upper())
    
    try:
        print(f" > Renaming the descriptor file at {id_number}/descriptor.mod")
        os.rename(f"{id_number}/descriptor.mod", f"{id_number}/{id_number}.mod")
        print(f" > Attempting to move {id_number}.mod")
        shutil.move(f"{id_number}/{id_number}.mod", f"{id_number}.mod")
        print(f" > Opening {id_number}.mod")
        with open(f"{id_number}.mod", "r") as descriptor:
            lines = [l.rstrip() for l in descriptor.readlines()]
            #Tests if it contains the Path="/foo/bar/baz" in the descriptor
            path_boolean = False
            file_id_boolean = False
            c = 0
            for line in lines:
                if line[:4] == "path": 
                    path_boolean = True
                    lines[c] = f"path=\"{os.path.normpath(os.path.join(PATH, id_number))}\"".replace("\\", "/")
                if line[:14] == "remote_file_id": 
                    file_id_boolean = True
                    lines[c] = f"remote_file_id=\"{id_number}\""
                c += 1
                
            if not path_boolean:
                lines.append(f"path=\"{os.path.normpath(os.path.join(PATH, id_number))}\"".replace("\\", "/"))
            if not file_id_boolean:
                lines.append(f"remote_file_id=\"{id_number}\"")

        print(" > Writing the descriptor file")
        with open(f"{id_number}.mod", "w") as descriptor:
            for line in lines:
                descriptor.write(line+"\n")
            
    except:
        print(f" ! Descriptor Error at file {id_number}.mod")
    count += 1

print(f"Succesful installation on all {count}/{max_count} mods!")