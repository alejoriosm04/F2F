document.addEventListener('DOMContentLoaded', () => {
    const generateButton = document.getElementById('generate-recipe-btn');
    generateButton.addEventListener('click', generateRecipe);
});

async function generateRecipe() {
    try {
        const response = await fetchRecipe();
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const titleOutput = document.getElementById('recipe-title');
        const recipeOutput = document.getElementById('recipe-output');
        titleOutput.textContent = data.title; 
        recipeOutput.innerHTML = data.recipe;
    } catch (error) {
        console.error('Error fetching recipe:', error.message);
    }
}

async function fetchRecipe() {
    const requestConfig = {
        method: 'GET',
        headers: {'X-Requested-With': 'XMLHttpRequest'},
    };
    return fetch('/recipe/generate_recipe/', requestConfig);
}

function updateRecipeContainer(recipe) {
    const container = document.getElementById('recipe-container');
    container.innerText = recipe;
}
