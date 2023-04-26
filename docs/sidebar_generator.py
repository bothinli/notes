import os

end_mark = '<!-- end_toc -->'


class Generator:

    @classmethod
    def get_file_toc_list(cls, path, exclude_dir=None, lstrip_path=None):
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
            if lstrip_path:
                link_url = link_url.lstrip(lstrip_path)

            if file_name.startswith(".") or file_name.startswith("_"):
                continue
            if os.path.isdir(url_path):
                tmp_lst = cls.get_file_toc_list(url_path, lstrip_path=lstrip_path)
                if tmp_lst:
                    file_toc_list.append(f"{' ' * 2 * url_path.count(os.sep)}" + f'- {file_name}')
                    file_toc_list.extend(tmp_lst)
                continue

            if file_name.endswith('.md'):  # 只处理.md
                title = os.path.split(file_name)[1].split('.')[0]
                file_toc_list.append(f"{' ' * 2 * url_path.count(os.sep)}" + f'- [{title}]({link_url})')

        return file_toc_list

    @staticmethod
    def get_h1_line(md_path):
        """.md获得文件内容的一级标题"""
        with open(md_path, 'r', encoding='utf8') as f:
            is_code_block = False  # 是否处于markdown代码区域

            for line in f.readlines():
                if not is_code_block and line.startswith('# '):
                    yield line.lstrip('# ').rstrip('\n')
                elif line.lstrip().startswith('```'):  # markdown代码区域
                    is_code_block = not is_code_block

    @staticmethod
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

    @classmethod
    def generate(cls, search_dir, generate_file_path=None, exclude_dir=None, lstrip_path=None):
        if generate_file_path is None:
            generate_file_path = 'README.md' if 'README.md' in os.listdir('.') else 'readme.md'

        file_toc_list = cls.get_file_toc_list(search_dir, exclude_dir=exclude_dir, lstrip_path=lstrip_path)
        for _ in file_toc_list:
            print(_)

        print(f'alter toc in {generate_file_path} after last ---')

        cls.alter_readme_toc(generate_file_path, file_toc_list)
        print('finished')


def main():
    Generator.generate("docs", "docs/_navbar.md", exclude_dir=["拉勾讲义", "README.md"], lstrip_path="docs")
    Generator.generate("docs", "docs/README.md", exclude_dir=["拉勾讲义", "README.md"], lstrip_path="docs")


if __name__ == '__main__':
    main()
