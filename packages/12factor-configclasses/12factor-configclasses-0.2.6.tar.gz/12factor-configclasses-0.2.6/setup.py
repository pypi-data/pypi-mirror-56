# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['configclasses']

package_data = \
{'': ['*']}

install_requires = \
['starlette>=0.12.12,<0.13.0']

extras_require = \
{'dotenv': ['python-dotenv[dotenv]>=0.10.3,<0.11.0'],
 'full': ['tomlkit[toml]>=0.5.8,<0.6.0',
          'python-dotenv[dotenv]>=0.10.3,<0.11.0',
          'pyyaml[yaml]>=5.1,<6.0'],
 'toml': ['tomlkit[toml]>=0.5.8,<0.6.0'],
 'yaml': ['pyyaml[yaml]>=5.1,<6.0']}

setup_kwargs = {
    'name': '12factor-configclasses',
    'version': '0.2.6',
    'description': 'Like dataclasses but for config.',
    'long_description': '# configclasses\n\n![PyPI](https://img.shields.io/pypi/v/12factor-configclasses)\n[![codecov](https://codecov.io/gh/kingoodie/configclasses/branch/master/graph/badge.svg)](https://codecov.io/gh/kingoodie/configclasses)\n<a href="https://codeclimate.com/github/kingoodie/configclasses/maintainability"><img src="https://api.codeclimate.com/v1/badges/9094f65f5caef64fb993/maintainability" /></a>\n\n\nLike dataclases but for config.\n\nSpecify your config with a class and load it with your env vars or env files.\n\n\n```python\n>>> import httpx\n... from configclasses import configclass\n>>> class UserAPIClient(httpx.AsyncClient):\n...     def __init__(self, config: ClientConfig, *args, **kwargs):\n...         self.config = config\n...         super().__init__(*args, **kwargs)\n... \n...     async def get_users(self, headers: Optional[Headers] = None) -> Dict[str, Any]:\n...         response = await self.get(f"{self.path}/users", auth=headers)\n...         response.raise_for_status()\n...         return response.json()\n...     \n>>> @configclass\n... class ClientConfig:\n...     host: str\n...     port: int\n...\n>>> config = ClientConfig.from_path(".env")\n... async with UserAPIClient(config) as client:\n...     users = await client.get_users(auth_headers)\n...   \n```\n\n## Features\n\n- Fill your configclasses with existent env vars.\n- Define default values in case these variables have no value at all.\n- Load your config files in env vars following [12factor apps](https://12factor.net) recommendations.\n- Support for _.env_, _yaml_, _toml_, _ini_ and _json_.\n- Convert your env vars with specified type in configclass: `int`, `float`, `str` or `bool`.\n- Use nested configclasses to more complex configurations.\n- Specify a prefix with `@configclass(prefix="<PREFIX>")` to append this prefix to your configclass\'  attribute names.\n- Config groups (__TODO__): https://cli.dev/docs/tutorial/config_groups/\n\n## Requirements\n\nPython 3.8+\n\n\n## Installation\n\n    pip install 12factor-configclasses\n    \n## Supported formats\n\n- .env ->   ```pip install 12factor-configclasses[dotenv]```\n- .yaml ->   ```pip install 12factor-configclasses[yaml]```\n- .toml ->   ```pip install 12factor-configclasses[toml]```\n- .ini\n- .json\n\nInstall all dependencies with:\n\n    pip install 12factor-configclasses[full]\n    \n## Example\n\n```.env\n# .env\nHOST=0.0.0.0\nPORT=8000\nDB_URL=sqlite://:memory:\nGENERATE_SCHEMAS=True\nDEBUG=True\nHTTPS_ONLY=False\nGZIP=True\nSENTRY=False\n```\n\n```python\n#config.py\nfrom configclasses import configclass\n\n\n@configclass\nclass DB:\n    user: str\n    password: str\n    url: str\n\n\n@configclass\nclass AppConfig:\n    host: str\n    port: int\n    db: DB\n    generate_schemas: bool\n    debug: bool\n    https_only: bool\n    gzip: bool\n    sentry: bool\n```\n\n```python\n# app.py\nfrom api.config import AppConfig\n\napp_config = AppConfig.from_path(".env")\napp = Starlette(debug=app_config.debug)\n\nif app_config.https_only:\n    app.add_middleware(\n        HTTPSRedirectMiddleware)\nif app_config.gzip:\n    app.add_middleware(GZipMiddleware)\nif app_config.sentry:\n    app.add_middleware(SentryAsgiMiddleware)\n\n...\n\nregister_tortoise(\n    app,\n    db_url=app_config.db.url,\n    modules={"models": ["api.models"]},\n    generate_schemas=app_config.generate_schemas,\n)\n\nif __name__ == "__main__":\n    uvicorn.run(app, host=app_config.host, port=app_config.port)\n```\n\n    \n',
    'author': 'Pablo Cabezas',
    'author_email': 'pabcabsal@gmail.com',
    'url': 'https://github.com/kingoodie/configclasses',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
