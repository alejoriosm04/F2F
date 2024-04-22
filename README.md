# FridgeToFeast <!-- omit from toc -->

- [Installation](#installation)


## Installation

1. Clone the repository.

2. [Create and activate a virtual
   environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments
   "venv — Creation of virtual environments &#8212; Python 3.12.2
   documentation") (optional, but strongly recommended).

3. Install dependencies with `pip install -r requirements.txt`

4. Set your OpenAI API key as an environment variable with `export OPENAI_API_KEY=your_api_key_here`

5. Apply migrations with `python manage.py migrate`

6. Create a superuser with `python manage.py createsuperuser`

7. Run `python manage.py runserver`

8. Access `localhost:8000` from a modern web browser.
