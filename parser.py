from bs4 import BeautifulSoup
from treelib import Tree


def read_html_as_fs_struct(filename: str) -> str:
    with open(filename, 'r') as filehandler:
        source_code = filehandler.read()
        
        return source_code


def put_tree_root(tree: Tree, soup: BeautifulSoup):

    for root in soup.find_all(recursive=False):
        if root.name == "html":         
            tree.create_node(tag="html", identifier="0_html", data=root)
    
            return root
        else:
            raise TreeRootException("Impossible to find the root.")
        

def put_tree_node_tag(tree: Tree, tag, parent_tag_id: str, all_tags: dict) -> None:
    tree.create_node(
            tag=tag.name, 
            identifier=f"{all_tags[tag.name]}_{tag.name}", 
            data=None,
            parent=parent_tag_id
        )


def put_tree_node_content(tree: Tree, parent_tag_id: str, all_tags: dict, content_data="") -> None:
    nid = all_tags["CONTENT"]
    
    tree.create_node(
         tag="CONTENT", 
         identifier=f"{nid}_CONTENT", 
         data=content_data, 
         parent=parent_tag_id
    )

    all_tags["CONTENT"] += 1


def put_tree_node_attr(tree: Tree, attr: str, parent_tag_id: str, all_tags: dict, attr_val="") -> None:
    nid = all_tags[attr]
    
    tree.create_node(
         tag=attr, 
         identifier=f"attr_{nid}_{attr}", 
         data=attr_val, 
         parent=parent_tag_id
    )

    all_tags[attr] += 1


def build_tree(tree: Tree, parent_tag, all_tags: dict) -> None:

    content = list(filter(lambda x: x != '\n', parent_tag.contents))

    if content:
        parent_tag_id = f"{all_tags[parent_tag.name]}_{parent_tag.name}"

        attrs = list(parent_tag.attrs.keys())

        if attrs:
            attr = attrs[-1]
            attr_val = parent_tag.attrs[attr] 

            if attr in all_tags:
                all_tags[attr] += 1
            else:
                all_tags[attr] = 0   

            put_tree_node_attr(tree, attr, parent_tag_id, all_tags, attr_val)

        tag_cnt = 0
        children_tags = parent_tag.findChildren(recursive=False)

        for elem in content:

            if elem in list(parent_tag.findAll(text=True, recursive=False)):
                if "CONTENT" in all_tags:
                    all_tags["CONTENT"] += 1
                else:
                    all_tags["CONTENT"] = 0  

                put_tree_node_content(tree, parent_tag_id, all_tags, elem)
            else: 
                tag = children_tags[tag_cnt]
                 
                if tag.name in all_tags:
                    all_tags[tag.name] += 1
                else:
                    all_tags[tag.name] = 0             

                itr = 0

                put_tree_node_tag(tree, tag, parent_tag_id, all_tags)

                build_tree(tree, tag, all_tags)    

                tag_cnt += 1                         
    else:
        return None


def get_tree(mount_fs_filename: str) -> Tree:
    fs_struct = read_html_as_fs_struct(mount_fs_filename)
    soup = BeautifulSoup(fs_struct, "html.parser") 

    tree = Tree()

    root = put_tree_root(tree, soup)

    all_tags = {"html": 0} 

    build_tree(tree, root, all_tags)

    return tree


class TreeRootException(Exception):
    pass
                
