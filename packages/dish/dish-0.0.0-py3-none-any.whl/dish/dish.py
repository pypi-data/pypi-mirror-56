from . import cli
from dulwich.repo import Repo
from dulwich.errors import NotGitRepository
from xml.parsers.expat import ParserCreate


DEFAULT_CONFIG = {
	'PS1': '$ ',
	'ALIASES': {},
}


class Dish():

	#: This is a dictionary of functions used to handle start tags in prompts.
	#: These functions accept one argument, which is a dictionary containing the
	#: XML tag's attributes. The function must return a string to replace the tag
	#: with.
	#:
	#: For example, when the prompt parser encounters ``<thing value="8">``, it
	#: will call ``self.start_tag_handlers['thing']({'value': '8'})``.
	start_tag_handlers = {}

	#: This is just like ``start_tag_handlers``, but it's for end tags, and the
	#: functions in it accept no arguments. If you want to create a self-closing
	#: tag, such as ``<cwd/>``, then you only need to add a function to
	#: ``start_tag_handlers``.
	end_tag_handlers = {}

	#: This is a dictionary of functions that accept no arguments and return a
	#: boolean value. These functions are used for ``<if_...>`` tags.
	prompt_predicates = {}

	def __init__(self):
		self.config = DEFAULT_CONFIG

		self.start_tag_handlers = {}
		self.end_tag_handlers = {}
		self.prompt_predicates = {}


	def run(self):
		cli.main.main(obj=self)


	def config_from_dict(self, d):
		self.config = {**self.config, **d}


	def reset_config(self):
		self.config = DEFAULT_CONFIG


	def register_extension(self, module, **kwargs):
		module.register_extension(self, **kwargs)


	def _handle_start_tag(self, name, attrs):
		if self._skip_this_data:
			return
		if name in self.start_tag_handlers:
			self._prompt_result += self.start_tag_handlers[name](attrs)
		elif name.startswith('if_'):
			if not self.prompt_predicates[name[3:]]():
				self._skip_this_data = True


	def _handle_end_tag(self, name):
		if name.startswith('if_'):
			self._skip_this_data = False
		elif self._skip_this_data:
			return
		elif name in self.end_tag_handlers:
			self._prompt_result += self.end_tag_handlers[name]()


	def _handle_text(self, data):
		if not self._skip_this_data:
			self._prompt_result += data


	def generate_prompt(self, prompt_type):
		self._prompt_result = ''
		self._skip_this_data = False # This is set to True by <if_...> tags if the condition is False, and tells _handle_text to ignore the stuff
		parser = ParserCreate()
		parser.StartElementHandler = self._handle_start_tag
		parser.EndElementHandler = self._handle_end_tag
		parser.CharacterDataHandler = self._handle_text
		parser.Parse(f'<prompt>{self.config[prompt_type]}</prompt>', True)
		return self._prompt_result


	@property
	def current_repo(self):
		try:
			return Repo('.')
		except NotGitRepository:
			return None
