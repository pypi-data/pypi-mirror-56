# TremTec CLI

As a TremTec Engineer, we need tools to make our daily work easier, because of that we've created the TremTec CLI, or just `ttc`. We intend to provider a lot of features like:

- **WorkSpace Management**: Create separated environments for your packages `pip`, `node`, and other languages.
- **Package Management**: Install, update and remove packages for your projects.
- **GitLab Integration**: You can create Merge Requests, test ci files, list docker register images, and a lot more from the cli.

## Usage

To install our cli tool, you need to:

```bash
pip install ttc
```

then you should configure you environment:

```bash
ttc configure
```

To see our command options, type

```bash
ttc --help
# or
ttc -h
```

## Add autocompletion

Just add to you `.bashrc` or `.zsh`:

```bash
eval "$(_TTC_COMPLETE=source ttc)"
eval "$(_TT_COMPLETE=source tt)"
```

### Dev mode

To install as a developer, first clone the project, go to a the cloned folder and then:

```bash
pip install -e '.[dev]'
```

##

Thanks for using tcc and have a happy code! 😊
