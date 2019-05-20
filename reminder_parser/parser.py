import markdown

md = markdown.Markdown(extensions = ['meta'])

f = open('Part3 Functions as Objects.md', 'r')
html = md.convert(f.read())
print(md.Meta)
