from __future__ import absolute_import
from hana.errors import HanaPluginError
from jinja2 import evalcontextfilter, Environment, FileSystemLoader, Markup
from jinja2.ext import Extension
import jinja2.exceptions
import json

# tojson filter in jinja sucks
@evalcontextfilter
def jinja_json(eval_ctx, value, indent=None):
    policies = eval_ctx.environment.policies
    dumper = policies['json.dumps_function']
    options = policies['json.dumps_kwargs']

    if indent is not None:
        options = dict(options)
        options['indent'] = indent

    if dumper is None:
        dumper = json.dumps

    rv = dumper(value, **options)

    return Markup(rv)

class Jinja():
    def __init__(self, config={}):

        #TODO: make sure required stuff is in config

        tplPath = config['directory']
        print "TPL PATH: %s" % tplPath

        extensions = [
            'jinja2.ext.do',
            'jinja2.ext.loopcontrols',
        ]

        self.config = {
            'extends_block': None,
        }

        self.config.update(config)

        self.env = Environment(loader=FileSystemLoader(tplPath),
                extensions=extensions)

        self.env.trim_blocks = True
        self.env.lstrip_blocks = True

        #TODO: adding custom filters
        self.env.filters['json'] = jinja_json

        #try:
        #    from typogrify.templatetags import jinja_filters
        #except ImportError:
        #    jinja_filters = False

        #if jinja_filters:
        #    jinja_filters.register(self.env)

    def __call__(self, files, hana):
        #print 'Jinja IS THERE: ', 'content/blog/2008/.DS_Store' in file_gen
        #TODO: this somehow fixes an issue where files are iterated through that no longer exist

        for filename, f in files:
            if 'index.' in filename:
                print 'jinja ', filename

            #TODO: this is not the nicest way of doing things... jekyll need it?
            if 'extends' in f and not 'template' in f:
                block_name = None

                if 'extends-block' in f:
                    block_name = f['extends-block']
                elif self.config['extends-block']:
                    block_name = self.config['extends-block']
                else:
                    raise Exception('missing extends block')

                f['template'] = True
                f['contents'] = "{{% extends '{:s}' %}}{{% block {:s} %}}{:s}{{% endblock %}}".format(f['extends'], block_name, f['contents'])


            if 'template' in f:
                c = self.render(filename, f, hana)
                f['contents'] = unicode(c)

    def render(self, filename, f, hana):
        tpl = f.get('template')
        template = None

        if tpl == True:
            #TODO: this doesn't give great feedback if there is an error in the template. The error wil be tracable to the template that got extended. Ideally we should identify where the string we are using as template came from
            template = self.env.from_string(f['contents'])
        else:
            template = self.env.get_template(tpl)

        try:
            return template.render(site=hana.metadata, page=f)
        except jinja2.exceptions.UndefinedError as e:
            print 'Jinja Debug', filename
            print f
            raise

