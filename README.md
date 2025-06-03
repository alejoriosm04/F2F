<h1 align="center">FridgeToFeast - FTF <img src=".github/images/isotype-ftf-cropped.png" width="60"/> </h1>

<p align="center"><i>Make the most of your food - Powered by AI</i></p>

## Contents <!-- omit in toc -->

- [About Us](#about-us)
  - [What is FTF?](#what-is-ftf)
  - [What do we solve?](#what-do-we-solve)
  - [Why use FTF?](#why-use-ftf)
- [Installation](#installation)
- [Authors](#authors)
- [License](#license)

## About Us

**FridgeToFeast (FTF)** is a project for the fourth-semester course "Integrative
Project II" (ST0251) taught at EAFIT University by professor Paola Vallejo, and
developed by Alejandro Ríos, Danniela Zárate, Luis Torres, and Sara Cortes.

### What is FTF?

FTF is an AI-based web application that analyzes kitchen ingredients to provide
a variety of tailored recipes, promoting efficient and healthy meal planning.

- **Optimized Recipes:** Simply add everything stored in your kitchen, and
  through our AI system, we can generate optimized recipes based on certain
  specifications such as preferences, quantities, type of cooking, etc.
- **Analytical Tools:** We also provide analytical tools to understand eating
  behavior.

### What do we solve?

FTF addresses the challenge of deciding what to cook with the available
ingredients, which can lead to unhealthy food choices and food waste. We seek to
optimize our users' food for optimal use.

### Why use FTF?

- **Powerful AI System:** For the creation of customized recipes.
- **Data Science and Analytics:** For understanding eating behaviors.
- **Resource Optimization:** To avoid waste.
- **User Support:** To get better food.
- **Time Reduction:** For cooking.
- **Simple and Engaging User Experience.**

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

For more detailed information about the project, please refer to the
[wiki](https://github.com/alejoriosm04/F2F/wiki).

## Authors

<a href="https://github.com/alejoriosm04/f2f">
  <img src="https://contrib.rocks/image?repo=alejoriosm04/f2f" />
</a>

## License

Copyright (c) 2024, Alejandro Rios, Danniela Zárate, Luis Torres, Sara Cortes.
All rights reserved FTF.
