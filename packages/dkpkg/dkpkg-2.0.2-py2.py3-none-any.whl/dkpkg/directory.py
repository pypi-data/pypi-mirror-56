# -*- coding: utf-8 -*-
"""
Programatic interface to package structure.

Use the :class:`Package` class.
"""
# pylint: disable=too-many-instance-attributes,too-many-locals,R0903,line-too-long
from __future__ import print_function
try:
    import ConfigParser as configparser
    from cStringIO import StringIO
except ImportError:  # pragma: nocover
    import configparser
    from io import StringIO

from dkfileutils.path import Path


class DefaultPackage(object):
    """Default package directory layout (consider this abstract, both in the
       sense that this class is abstract and in the sense that this is the
       attribute names of this object, not neccessarily the actual directory
       name)

      ::

          <parent>                    # self.location (abspath)
             |--<name>                # self.root (abspath), self.package_name
                |-- <name>            # <name> == self.name, self.source
                |   |-- static        # self.django_static
                |   `-- templates     # self.django_templates
                |-- js                # self.source_js
                |-- less              # self.source_less
                |-- docs              # self.docs
                +-- tests             # self.tests
                |-- build             # self.build
                |   |-- coverage      # self.build_coverage
                |   |-- docs          # self.build_docs
                |   |-- lintscore     # self.build_lintscore
                |   |-- meta          # self.build_meta
                |   `-- pytest        # self.build_pytest
                +-- setup.py          #
                `-- requirements.txt  #

    """
    #: A set of all overridable keys
    KEYS = {
        'location',
        'package_name',
        'name',
        'docs',
        'tests',
        'tests_js',
        'build',
        'source',
        'source_js',
        'source_less',
        'django_templates',
        'django_static',
        'django_models',
        'build_coverage',
        'build_docs',
        'build_lintscore',
        'build_meta',
        'build_pytest',
    }

    def __init__(self, root, **kw):
        #: The abspath to the "working copy".
        self.root = kw.get('root') or Path(root).abspath()
        #: The abspath of the directory containing the root.
        self.location = kw.get('location') or self.root.parent  # pylint: disable=no-member
        #: The pip-installable name.
        self.package_name = kw.get('package_name') or self.root.basename()
        #: The importable name.
        self.name = kw.get('name') or self.package_name.replace('-', '')
        #: The documentation source directory.
        self.docs = kw.get('docs') or self.root / 'docs'
        #: The tests directory.
        self.tests = kw.get('tests') or self.root / 'tests'
        #: the javascript tests directory
        self.tests_js = kw.get('tests_js') or self.root / 'tests' / 'js'
        #: The root of the build output directory.
        self.build = kw.get('build') or self.root / 'build'
        #: The source directory.
        self.source = kw.get('source') or self.root / self.name

        #: The javascript source directory.
        self.source_js = kw.get('source_js') or self.root / 'js'
        #: The less source directory.
        self.source_less = kw.get('source_less') or self.root / 'less'

        #: The django app template directory.
        self.django_templates = kw.get('django_templates') or self.root / self.name / 'templates'
        #: The django app static directory.
        self.django_static = kw.get('django_static') or self.root / self.name / 'static'

        #: The django models directory
        self.django_models_dir = kw.get('django_models') or self.root / self.name / 'models'
        #: the django models.py file
        self.django_models_py = kw.get('django_models') or self.root / self.name / 'models.py'

        #: Coverage output directory.
        self.build_coverage = kw.get('build_coverage') or self.root / 'build' / 'coverage'
        #: Documentation output directory.
        self.build_docs = kw.get('build_docs') or self.root / 'build' / 'docs'
        #: Lintscore output directory.
        self.build_lintscore = kw.get('build_lintscore') or self.root / 'build' / 'lintscore'
        #: Package meta output directory.
        self.build_meta = kw.get('build_meta') or self.root / 'build' / 'meta'
        #: Pytest output directory.
        self.build_pytest = kw.get('build_pytest') or self.root / 'build' / 'pytest'
        #: Gitlab public directory.
        self.public_dir = kw.get('public_dir') or self.root / 'public'

        for k, v in kw.items():
            setattr(self, k, v)

    def is_django(self):
        """Is this a Django package?
        """
        return any(d is not None and d.exists() for d in self.django_dirs)

    @property
    def source_dirs(self):
        """Directories containing source.
        """
        return [self.source, self.source_js, self.source_less]

    @property
    def django_models(self):
        """Return the path to the Django models.
        """
        if self.django_models_dir.exists():
            return self.django_models_dir
        if self.django_models_py.exists():
            return self.django_models_py
        return None

    @property
    def django_dirs(self):
        """Directories containing/holding django specific files.
        """
        return [self.django_static, self.django_templates, self.django_models]

    @property
    def build_dirs(self):
        """Directories containing build artifacts.
        """
        return [self.build, self.build_coverage, self.build_docs,
                self.build_lintscore, self.build_meta, self.build_pytest]

    @property
    def all_dirs(self):
        """Return all package directories.
        """
        return ([self.docs, self.tests]
                + self.source_dirs
                + self.django_dirs
                + self.build_dirs)

    def missing_dirs(self):
        """Return all missing directories.
        """
        return [d for d in self.all_dirs if d is not None and not d.exists()]

    def make_missing(self):
        """Create all missing directories.
        """
        for d in self.missing_dirs():
            d.makedirs()

    def __repr__(self):
        keylen = max(len(k) for k in self.__dict__.keys())
        # vallen = max(len(k) for k in self.__dict__.values())
        lines = []
        for k, v in sorted(self.__dict__.items()):
            lines.append("%*s %-s" % (keylen, k, v))
        return '\n'.join(lines)

    def write_ini(self, _fname, section):
        """Write to ini file.
        """
        cp = configparser.RawConfigParser()
        cp.add_section(section)
        vals = [
            'root', 'location', 'name', 'docs', 'tests', 'source', 'source_js',
            'source_less', 'build', 'build_coverage', 'build_docs',
            'build_lintscore', 'build_meta', 'build_pytest',
            'django_templates', 'django_static',
        ]
        for val in vals:
            cp.set(section, val, getattr(self, val))

        out = StringIO()
        cp.write(out)
        return out.getvalue()


class Package(DefaultPackage):
    """Package layout with possible overrides.
    """

    def __init__(self, root, **kw):
        # name=None,
        # docs=None,
        # tests=None,
        # build=None,
        # source=None,
        # source_js=None,
        # source_less=None,
        # build_coverage=None,
        # build_docs=None,
        # build_lintscore=None,
        # build_meta=None,
        # build_pytest=None,
        # django_templates=None,
        # django_static=None,
        # pylint: disable=multiple-statements,too-many-arguments,R0912
        super(Package, self).__init__(root, **kw)

        name = kw.get('name')
        docs = kw.get('docs')
        tests = kw.get('tests')
        build = kw.get('build')
        source = kw.get('source')
        source_js = kw.get('source_js')
        source_less = kw.get('source_less')
        source_styles = kw.get('styles')
        build_coverage = kw.get('build_coverage')
        build_docs = kw.get('build_docs')
        build_lintscore = kw.get('build_lintscore')
        build_meta = kw.get('build_meta')
        build_pytest = kw.get('build_pytest')
        django_templates = kw.get('django_templates')
        django_static = kw.get('django_static')

        if name: self.name = name
        if docs: self.docs = docs
        if tests: self.tests = tests
        self.source_js = self.root / 'js'

        self.source_less = self.root / 'less'
        if build:
            self.build = build
            self.build_coverage = self.build / 'coverage'
            self.build_docs = self.build / 'docs'
            self.build_lintscore = self.build / 'lintscore'
            self.build_meta = self.build / 'meta'
            self.build_pytest = self.build / 'pytest'
        if source:
            self.source = source
            self.django_templates = self.source / 'templates'
            self.django_static = self.source / 'static'
        if source_js: self.source_js = source_js
        if source_less: self.source_styles = source_less
        if source_styles: self.source_styles = source_styles
        if build_coverage: self.build_coverage = build_coverage
        if build_docs: self.build_docs = build_docs
        if build_lintscore: self.build_lintscore = build_lintscore
        if build_meta: self.build_meta = build_meta
        if build_pytest: self.build_pytest = build_pytest
        if django_templates: self.django_templates = django_templates
        if django_static: self.django_static = django_static

        # dkcode.Package compatibility
        self.build_dir = self.build
        self.lintscore_dir = self.build_lintscore
        self.meta_dir = self.build_meta
        self.coverage = self.build_coverage
        self.coverage_dir = self.build_coverage
        self.docs_dir = self.docs
        self.package_dir = self.root
        self.tests_dir = self.tests
        self.pyroot_dir = self.root
        self.source_dir = self.source
        self.public = self.public_dir
        self.pytest_dir = self.build_pytest
        self.static_dir = self.django_static
        self.templates_dir = self.django_templates
