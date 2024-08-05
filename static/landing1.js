document.addEventListener('DOMContentLoaded', () => {
    const searchBar = document.querySelector('.search-bar input');
    const searchButton = document.querySelector('.search-bar button');

    function handleSearch() {
        const problem = searchBar.value.trim();
        if (problem) {
            localStorage.setItem('currentProblem', problem);
            localStorage.setItem('problemType', 'Unknown');
            window.location.href = '/output';
        }
    }

    searchBar.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });

    searchButton.addEventListener('click', handleSearch);
});