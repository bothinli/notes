"""
extract all markdown h1 in docs/doc folder;
insert/alter into top of the readme.md/README.MD with link;
end with '<!-- end_toc -->'
tree like
docs/
├── api.md
├── change_log.md
├── deep_docs/
│         ├── api.md
│         ├── change_log.md
│         └── quick_start.md
├──quick_start.md
└──readme.md
"""
import os

end_mark = '<!-- end_toc -->'


def get_file_toc_list(path, exclude_dir=None):
    """获得文件标题（.md文件链接 + .md文件内容的一级标题）"""
    if exclude_dir is None:
        exclude_dir = []
    file_toc_list = []
    for file_name in os.listdir(path):
        if file_name in exclude_dir:
            continue

        url_path = file_name.replace(os.sep, '/')
        if path != '.':
            url_path = os.path.join(path, url_path)
        link_url = url_path.replace(os.sep, '/')

        if file_name.startswith("."):
            continue
        if os.path.isdir(url_path):
            tmp_lst = get_file_toc_list(url_path)
            if tmp_lst:
                file_toc_list.append(f"{' ' * 2 * url_path.count(os.sep)}" + f'- [{file_name}]({link_url})')
                file_toc_list.extend(tmp_lst)
            continue

        if file_name.endswith('.md'):  # 只处理.md
            title = os.path.split(file_name)[1].split('.')[0]
            file_toc_list.append(f"{' ' * 2 * url_path.count(os.sep)}" + f'- [{title}]({link_url})')
            # 处理h1标题
            # for h1_in_md in get_h1_line(file_path):
            #     if h1_in_md:  # 过滤没有h1的
            #         h1_list.append(
            #             f"{' ' * 2 * file_path.count(os.sep)}" + f'- [{h1_in_md}]({url_path}#{h1_in_md})')
    return file_toc_list


def get_h1_line(md_path):
    """.md获得文件内容的一级标题"""
    with open(md_path, 'r', encoding='utf8') as f:
        is_code_block = False  # 是否处于markdown代码区域

        for line in f.readlines():
            if not is_code_block and line.startswith('# '):
                yield line.lstrip('# ').rstrip('\n')
            elif line.lstrip().startswith('```'):  # markdown代码区域
                is_code_block = not is_code_block


def alter_readme_toc(file, new_h1_list):
    """添加/修改README.md中的目录"""
    with open(file, "r", encoding="utf-8") as f1:
        content = f1.read()
    l_loc = content.find(end_mark)
    if l_loc == -1:
        content = '\n'.join(new_h1_list) + '\n' + end_mark + '\n' + content

    else:
        content = '\n'.join(new_h1_list) + '\n' + end_mark + '\n' + content[l_loc + len(end_mark) + 1:]

    with open(file, "w", encoding="utf-8") as f:
        f.write(content)


def main(search_dir, generate_file_path=None, exclude_dir=None):
    if generate_file_path is None:
        generate_file_path = 'README.md' if 'README.md' in os.listdir('.') else 'readme.md'

    file_toc_list = get_file_toc_list(search_dir, exclude_dir=exclude_dir)
    for _ in file_toc_list:
        print(_)

    print(f'alter toc in {generate_file_path} after last ---')

    alter_readme_toc(generate_file_path, file_toc_list)
    print('finished')


if __name__ == '__main__':
    # main("docs", exclude_dir=["拉勾讲义"])
    main("docs", "docs/_sidebar.md", exclude_dir=["拉勾讲义"])
