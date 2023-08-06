# UQtie

Utilities for Qt

A small set of features to make it easier to use PyQt5. Implements
a repetive pattern for quickly building throwaway or small
Qt applications. Features include Font Selection, Zoom In/Out,
and geometry persistence.

## Getting Started

### Prerequisites

* [PyQt5](https://pypi.org/project/PyQt5/) is obviously required.

The **uqtie** distribution package does not name *PyQt5* as a dependency
because you may have already installed it in some custom way, and
you don't want the **uqtie** installation process to create a redundant
*PyQt5* installation.

If you don't already have it, you can install **PyQt5** by doing this:

```bash
pip install pyqt5
```

Be aware that the appropriate installation procedure for a package can
vary depending on your OS and other factors.

### Installing uqtie

Install the package:

```bash
pip install uqtie
```

Or clone from GitHub:

```bash
git clone https://github.com/langrind/uqtie.git
```

and then run the setup script:

```bash
python setup.py
```

To show **uqtie** in action, run `simple_uqtie.py`. It's a do-nothing app,
the lets you select the font from the File menu, or zoom via the View menu.
It's copied in your $PATH when you install the **UQtie** package.

## Tests

There are no tests yet, beyond running `simple_uqtie.py`.

## Deployment

TBS: details about usage in different OS environments

## Using UQtie

| Module Name   | Purpose                                                         |
+---------------+-----------------------------------------------------------------|
| UqtMav        | UqtMavConn allows easy use of pymavlink connections in Qt app   |
| UqtWin        | MainWindow class provides an app main window with features      |
| UqtStylesheet | Allows app to maintain a QSS file with variable properties -    |
|               | a "poor man's SASS"                                             |

You can view the source of `simple_uqtie.py ` in the `example/` subdirectory of the repo.

There are three items of note:

1) Import the `UqtWin` module:
    ```
	
    from   uqtie import UqtWin
    
    ```
1) Define a subclass of `MainWindow`
    ```
	
	class TestAppMainWindow(UqtWin.MainWindow):
        def __init__(self, parsedArgs, **kwargs ):
            super(TestAppMainWindow, self).__init__(parsedArgs, **kwargs)
	
	```
1) Instantiate the subclass
    ```

    # can add optional title='<OptionalTitle>' if it is different from your app name
    mainw = TestAppMainWindow(parsedArgs, app=app, organizationName='Craton', appName='UqtTest')

```

For more info, [RTFD](http://uqtie.rtfd.io/).

## Contributing

This project is *ad hoc* in nature, so I don't foresee contributions. Nevertheless,
feel free to make a pull request.

## Versioning

Versions are assigned in accordance with [Semantic Versioning](http://semver.org/).
For the versions available, see the [tags on this repository](https://github.com/langrind/uqtie/tags).

## Pronunciation

* "**uqtie**" is pronounced *You Cutie* :heart_eyes:
* "**Uqt**", used as a prefix in the code, rhymes with "duct" 

## Authors

* **[Nik Langrind](https://github.com/langrind)** - *Sole author*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* I used the **PurpleBooth** [README template](https://github.com/PurpleBooth/a-good-readme-template)
