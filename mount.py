import argparse
import os

from parser import get_tree


def file_system_mounter(tree, parent_id, path):
    children_nodes = tree.children(parent_id)

    if children_nodes:
        num = 1
        for node in children_nodes:
            f_path = "" + path

            if not node.data:
                folder_name = f"{num}_{node.tag}"
                f_path += "/{0}".format(folder_name)

                os.mkdir(f_path)
            elif node.identifier[:5] == "attr_":
                filename = "{0}/{1}".format(f_path, node.tag)
                with open(filename, 'w') as filehandler:
                    filehandler.write(node.data)
            else:
                filename = "{0}/{1}".format(f_path, f"{num}_{node.tag}")
                with open(filename, 'w') as filehandler:
                    filehandler.write(node.data)

            file_system_mounter(tree, node.identifier, f_path)
            num += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--path", default=".", type=str, help="Input path for mount")

    args = parser.parse_args()

    tree = get_tree("mount_fs.html")
    root = tree.root

    path = args.path

    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    
    file_system_mounter(tree, root, path)
