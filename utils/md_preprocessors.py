import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class CodeBlockExtension(Extension):
    """ Добавляет кодовый блок. """
    def extendMarkdown(self, md):
        md.preprocessors.register(CodeBlockPreprocessor(md), 'code_block', 25)


class CodeBlockPreprocessor(Preprocessor):
    CODE_BLOCK_RE = re.compile(r'^```(\w+)\n(.*?)\n```$', re.MULTILINE | re.DOTALL)

    def run(self, lines):
        new_lines = []
        in_code_block = False

        for line in lines:
            if not in_code_block:
                match = self.CODE_BLOCK_RE.match(line)
                if match:
                    lang = match.group(1)
                    code = match.group(2)
                    new_lines.append('<pre><code class="language-{0}">'.format(lang))
                    new_lines.append(code)
                    in_code_block = True
                    continue

            if in_code_block:
                if line.strip() == '```':
                    new_lines.append('</code></pre>')
                    in_code_block = False
                    continue

                if line.strip() == '```python':
                    new_lines.append('</code></pre>')
                    new_lines.append('<pre><code class="language-python">')
                    continue

            new_lines.append(line)

        return new_lines
