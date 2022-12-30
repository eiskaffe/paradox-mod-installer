import os
import shutil

parent_dir = os.path.split(__file__)[0]

_, dirs, _ = next(os.walk(parent_dir))

# id_number = directory's name
for id_number in dirs:
    try:
        shutil.move(os.path.join(parent_dir, id_number, "descriptor.mod"), os.path.join(parent_dir, f"{id_number}.mod"))
        
        with open(os.path.join(parent_dir, f"{id_number}.mod"), "r") as descriptor:
            lines = [l.rstrip() for l in descriptor.readlines()]
            #Tests if it contains the Path="/foo/bar/baz" in the descriptor
            path_boolean = False
            file_id_boolean = False
            c = 0
            for line in lines:
                if line[:4] == "path": 
                    path_boolean = True
                    lines[c] = f"path=\"{os.path.normpath(os.path.join(parent_dir, id_number))}\"".replace("\\", "/")
                if line[:14] == "remote_file_id": 
                    file_id_boolean = True
                    lines[c] = f"remote_file_id=\"{id_number}\""
                c += 1
                
            if not path_boolean:
                lines.append(f"path=\"{os.path.normpath(os.path.join(parent_dir, id_number))}\"".replace("\\", "/"))
            if not file_id_boolean:
                lines.append(f"remote_file_id=\"{id_number}\"")

        print(" > Writing the descriptor file")
        with open(os.path.join(parent_dir, f"{id_number}.mod"), "w") as descriptor:
            for line in lines:
                descriptor.write(line+"\n")
    except FileNotFoundError:
        print(f"Passing {id_number}")


