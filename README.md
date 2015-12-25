# koto
Track email communications from the command line.

Currently only compatible with gmail accounts.  Tested on OSX 10.10.5 

#Installation

```
$pip install koto
```

It's my first time using pip, so every dependency may not have been packaged.

Let me know which packages were not included.


#Usage

Build a list of contacts by adding each person individually.  Email is an optional argument, but highly recommended.

```
$koto add <firstname> <lastname> [<email>]
```

You can also import a list of contacts in CSV format.  The `import` command will guide you through the process.

```
$koto import
````

The `status` command kinda sucks right now, but you can still use it.  The most useful command is `list -t`

I'll make the readme better later.  To learn more about command usage:

```
$koto --help
```

#Planned features

- `koto commit <firstname> [<lastname>] <commit>`
- Comprehensive `koto status` command w/ commit tree branches
- Day -> month parser w/ hour support
